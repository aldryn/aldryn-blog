from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import get_language

from hvad.utils import get_translation

from .conf import settings


def get_blog_languages():
    from .models import Post

    langs = []
    for post in Post.objects.all():
        if not post.language:
            # at least one post is available in all languages
            return settings.languages
        if post.language not in langs:
            langs.append(post.language)
    return langs


def get_blog_authors():
    now = timezone.now()
    return User.objects.filter(
        (Q(post__publication_end__isnull=True) | Q(post__publication_end__gte=now))
        & (Q(post__language=get_language()) | Q(post__language__isnull=True))
        & Q(post__publication_start__lte=now)
    ).distinct()


def generate_slugs(users):
    """
    Takes a queryset of users and creates nice slugs
    Returns the same queryset but with a slug attribute on each user
    """

    slugs = []
    slugged_users = []

    for user in users:
        slug = ''
        _slug = slugify(user.get_full_name())
        if not _slug:
            slug = user.get_username()

        elif not _slug in slugs:
            slug = _slug

        else:
            for i in xrange(2, 100):
                if not '%s-%i' % (_slug, i) in slugs:
                    slug = '%s-%i' % (_slug, i)
                    break

        if not slug:
            slug = user.get_username()

        slugs.append(slug)
        user.slug = slug
        slugged_users.append(user)

    return slugged_users


def get_user_from_slug(find_slug):
    authors = generate_slugs(get_blog_authors())
    for author in authors:
        if author.slug == find_slug:
            return author
    return None


def get_slug_for_user(find_user):
    authors = generate_slugs(get_blog_authors())
    for author in authors:
        if author == find_user:
            return author.slug


def get_slug_in_language(record, language):
    if not record:
        return None
    if hasattr(record, record._meta.translations_cache) and language == record.language_code:  # possibly no need to hit db, try cache
        return record.lazy_translation_getter('slug')
    else:  # hit db
        try:
            translation = get_translation(record, language_code=language)
        except ObjectDoesNotExist:
            return None
        else:
            return translation.slug
