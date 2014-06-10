===============
Aldryn Blog App
===============

Simple blogging application. It allows you to:

- write a tagable post message
- plug in latest post messages (optionally filtered by tags)
- attach post message archive view

Installation
============

Aldryn Platform Users
---------------------

Choose a site you want to install the add-on to from the dashboard. Then go to ``Apps -> Install app`` and click ``Install`` next to ``Blog`` app.

Redeploy the site.

Manual Installation
-------------------

**NOTE**: If you are using a database other than PostgresSQL, check out the table below.

Database support:

+---------------+----------------------------+-----------------+
| SQLite3       | MySQL                      | PostgresSQL     |
+===============+============================+=================+
| Not supported | Requires Time zone support | Fully supported |
+---------------+----------------------------+-----------------+


Run ``pip install aldryn-blog``.

Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        
        'aldryn_blog',
        'aldryn_common',
        'django_select2',
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'filer',
        'taggit',
        # for search
        'aldryn_search',
        'haystack',
        …
    ]

Posting
=======

You can add post messages in the admin interface now. Search for the label ``Aldryn_Blog``.

In order to display them, create a CMS page and install the app there (choose ``Blog`` from the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS site has become a blog post archive view.

About the Content of a Post
---------------------------

In Aldryn Blog, there are two content fields in each Post which may be confusing:

1. Lead-In and
2. Body

The Lead-In is text/html only and is intended to be a brief "teaser" or introduction into the blog post. The lead-in is shown in the blog list-views and is presented as the first paragraph (or so) of the blog post itself. **It is not intended to be the whole blog post.**

To add the body of the blog post, the CMS operator will:

1. Navigate to the blog post view (*not* the list view);
2. Click the "Live" button in the CMS toolbar to go into edit-mode;
3. Click the "Structure" button to enter the structure sub-mode;
4. Here the operator will see the placeholder "ALDRYN_BLOG_POST_CONTENT", use the menu on the far right of the placeholder to add whatever CMS plugin the operator wishes –– this will often be the Text plugin;
5. Double-click the new Text plugin (or whatever was selected) to add the desired content;
6. Save changes on the plugin's UI;
7. Press the "Publish" button in the CMS Toolbar.


Available CMS Plug-ins
======================

* ``Latest Blog Entries`` plugin lets you list **n** most frequent blog entries filtered by tags.
* ``Blog Authors`` plugin lists blog authors and the number of posts they have authored.
* ``Tags`` plugin lists the tags applied to all posts and allows filtering by these tags.


Search
======

If you want the blog posts to be searchable, be sure to install ``aldryn-search`` and its dependencies.
Your posts will be searchable using ``django-haystack``.

You can turn it this behavior off by setting ``ALDRYN_BLOG_SEARCH = False`` in your django settings.


Additional Settings
===================

* ``ALDRYN_BLOG_SHOW_ALL_LANGUAGES``: By default, only the blog posts in the current language will be displayed. By setting the value of this option to ``True``, you can change the behaviour to display all posts from all languages instead.
* ``ALDRYN_BLOG_USE_RAW_ID_FIELDS``: Enable raw ID fields in admin (default = False)
