# -*- coding: utf-8 -*-
import datetime
from collections import Counter

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _, override

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager
from taggit.models import TaggedItem, Tag

from .conf import settings
from .utils import generate_slugs, get_blog_authors, get_slug_for_user


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class RelatedManager(models.Manager):

    def get_query_set(self):
        qs = super(RelatedManager, self).get_query_set()
        return qs.select_related('key_visual')

    def filter_by_language(self, language):
        qs = self.get_query_set()
        return qs.filter(Q(language__isnull=True) | Q(language=language))

    def filter_by_current_language(self):
        return self.filter_by_language(get_language())

    def get_tags(self, language):
        """Returns tags used to tag post and its count. Results are ordered by count."""

        # get tagged post
        entries = self.filter_by_language(language).distinct()
        if not entries:
            return []
        kwargs = TaggedItem.bulk_lookup_kwargs(entries)

        # aggregate and sort
        counted_tags = dict(TaggedItem.objects
                                      .filter(**kwargs)
                                      .values('tag')
                                      .annotate(count=models.Count('tag'))
                                      .values_list('tag', 'count'))

        # and finally get the results
        tags = Tag.objects.filter(pk__in=counted_tags.keys())
        for tag in tags:
            tag.count = counted_tags[tag.pk]
        return sorted(tags, key=lambda x: -x.count)

    def get_months(self, language):
        """Get months with aggregatet count (how much posts is in the month). Results are ordered by date."""
        # done via naive way as django's having tough time while aggregating on date fields
        entries = self.filter_by_language(language)
        dates = entries.values_list('publication_start', flat=True)
        dates = [(x.year, x.month) for x in dates]
        date_counter = Counter(dates)
        dates = set(dates)
        dates = sorted(dates, reverse=True)
        return [{'date': datetime.date(year=year, month=month, day=1),
                 'count': date_counter[year, month]} for year, month in dates]


class PublishedManager(RelatedManager):

    def get_query_set(self):
        qs = super(PublishedManager, self).get_query_set()
        now = timezone.now()
        qs = qs.filter(publication_start__lte=now)
        qs = qs.filter(Q(publication_end__isnull=True) | Q(publication_end__gte=now))
        return qs


class Post(models.Model):

    title = models.CharField(_('Title'), max_length=255)
    slug = models.CharField(_('Slug'), max_length=255, unique=True, blank=True,
                            help_text=_('Used in the URL. If changed, the URL will change. '
                                        'Clean it to have it re-created.'))
    language = models.CharField(_('language'), max_length=5, null=True, blank=True, choices=settings.LANGUAGES,
                                help_text=_('leave empty to display in all languages'))
    key_visual = FilerImageField(verbose_name=_('Key Visual'), blank=True, null=True)
    lead_in = HTMLField(_('Lead-in'),
                        help_text=_('Will be displayed in lists, and at the start of the detail page (in bold)'))
    content = PlaceholderField('aldryn_blog_post_content', related_name='aldryn_blog_posts')
    author = models.ForeignKey(to=AUTH_USER_MODEL, verbose_name=_('Author'))
    publication_start = models.DateTimeField(_('Published Since'), default=timezone.now,
                                             help_text=_('Used in the URL. If changed, the URL will change.'))
    publication_end = models.DateTimeField(_('Published Until'), null=True, blank=True)

    objects = RelatedManager()
    published = PublishedManager()
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'year': self.publication_start.year,
                  'month': self.publication_start.month,
                  'day': self.publication_start.day,
                  'slug': self.slug}
        if self.language:
            with override(self.language):
                return reverse('aldryn_blog:post-detail', kwargs=kwargs)
        return reverse('aldryn_blog:post-detail', kwargs=kwargs)

    class Meta:
        ordering = ['-publication_start']

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(**kwargs)

    def get_author_slug(self):
        # FIXME: This is a potential performance hogger
        return get_slug_for_user(self.author)


class LatestEntriesPlugin(CMSPlugin):

    latest_entries = models.IntegerField(default=5, help_text=_('The number of latests entries to be displayed.'))
    tags = models.ManyToManyField('taggit.Tag', blank=True, help_text=_('Show only the blog posts tagged with chosen tags.'))

    def __unicode__(self):
        """
        must return a unicode string
        """
        return str(self.latest_entries).decode('utf8')

    def copy_relations(self, oldinstance):
        self.tags = oldinstance.tags.all()

    def get_posts(self):
        posts = Post.published.filter_by_language(self.language)
        tags = list(self.tags.all())
        if tags:
            posts = posts.filter(tags__in=tags)
        return posts[:self.latest_entries]


class AuthorsPlugin(CMSPlugin):
    def get_authors(self):
        return generate_slugs(get_blog_authors())


def force_language(sender, instance, **kwargs):
    if issubclass(sender, CMSPlugin) and instance.placeholder and instance.placeholder.slot == 'aldryn_blog_post_content':
        instance.language = settings.ALDRYN_BLOG_PLUGIN_LANGUAGE


for model in CMSPlugin.__subclasses__():
    models.signals.pre_save.connect(force_language, sender=model)
