from unittest import TestCase

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from cms import api
from cms.utils import get_cms_setting

from .models import Post


class EventAddTest(TestCase):
    su_username = 'user'
    su_password = 'pass'

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            apphook='BlogApp', apphook_namespace='Blog'
        )
        self.placeholder = self.page.placeholders.all()[0]
        self.user = User.objects.create(first_name='Peter', last_name='Muster')

    def test_create_post(self):
        """
        We can create a blog post
        """
        title = 'First'
        before_count = Post.objects.count()
        Post.objects.create(title=title, slug='first-blog', author=self.user)
        after_count = Post.objects.count()
        self.assertEqual(before_count + 1, after_count)

    def test_delete_post(self):
        """
        We can delete a blog
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
        We'll create an Post with a pasted end and check if it isn't shown
        """
        title = 'Past Blog Post'
        date = timezone.now() - timezone.timedelta(minutes=1)

        post = Post.objects.create(
            title=title, slug='past-blog',
            publication_end=date, author=self.user
        )

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 404)