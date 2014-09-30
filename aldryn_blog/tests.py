from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import override

from cms import api
from cms.utils import get_cms_setting

from .models import Post, Category


class PostAddTest(TestCase):
    su_username = 'user'
    su_password = 'pass'

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            apphook='BlogApp', apphook_namespace='Blog'
        )
        api.create_title('fr', 'french page', self.page)
        self.page.publish('fr')
        self.placeholder = self.page.placeholders.all()[0]
        self.user = User.objects.create(first_name='Peter', last_name='Muster')

    def test_create_post(self):
        """
        We can create a post
        """
        title = 'First'
        post = Post.objects.create(title=title, slug='first-blog', author=self.user)
        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, title)

    def test_delete_post(self):
        """
        We can delete a post
        """
        title = 'Delete Post'
        Post.objects.create(title=title, author=self.user)
        Post.objects.get(title=title).delete()
        self.assertFalse(Post.objects.filter(title=title))

    def test_publication_start(self):
        """
        We'll create a Post with a future start & end and check if it is shown
        """
        title = 'Future Blog Post'
        date = timezone.now()

        post = Post.objects.create(
            title=title, slug='future-blog', publication_start=date,
            publication_end=date + timezone.timedelta(days=1),
            author=self.user
        )

        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, title)

    def test_publication_end(self):
        """
        We'll create an Post with a past end and check if it isn't shown
        """
        title = 'Past Blog Post'
        date = timezone.now() - timezone.timedelta(minutes=1)

        post = Post.objects.create(
            title=title, slug='past-blog',
            publication_end=date, author=self.user
        )

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_has_content(self):
        """
        We check if the post has content
        """
        title = 'Post Title'
        content = 'Lorem Ipsum Dolor'

        post = Post.objects.create(
            title=title,
            author=self.user
        )

        api.add_plugin(post.content, 'TextPlugin', self.language)
        plugin = post.content.get_plugins()[0].get_plugin_instance()[0]
        plugin.body = content
        plugin.save()

        response = self.client.get(post.get_absolute_url())

        self.assertContains(response, content)
        self.assertContains(response, title)

    def test_category(self):
        """
        We create a Post with a category
        """
        category = Category.objects.create(
            name='Sport',
            slug='sport',
        )

        post = Post.objects.create(
            title='My Post title',
            category=category, author=self.user
        )

        kwargs = {
            'category': category.slug
        }

        url = reverse('aldryn_blog:category-posts', kwargs=kwargs)
        response = self.client.get(url)
        self.assertContains(response, post.title)

    def test_language(self):
        """
        if the wrong language is set in the url we should get a redirect to the main homepage
        """

        title = 'French Blog Post'

        post = Post.objects.create(
            title=title, slug='french-post',
            author=self.user, language='fr',
        )

        with override('fr'):
            # List View
            url = reverse('aldryn_blog:latest-posts')
            response = self.client.get(url)
            self.assertContains(response, title)

            # Detail View
            url = post.get_absolute_url()
            response = self.client.get(url)
            self.assertContains(response, title)

        with override('en'):
            # List View
            url = reverse('aldryn_blog:latest-posts')
            response = self.client.get(url)
            self.assertNotContains(response, title)

            with self.settings(ALDRYN_BLOG_SHOW_ALL_LANGUAGES=True):
                response = self.client.get(url)
                self.assertContains(response, title)

            # Detail View
            # Does not raise - not sure if intended?
            # self.assertRaises(NoReverseMatch, post.get_absolute_url)
