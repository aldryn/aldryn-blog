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

**NOTE: At this time, the ``Latest Blog Entries`` CMSPlugin, and possibly other portions do not work with SQLite3 databases and requires that Time Zone Support is added to MySQL Installations. No special considerations are required, however, for Postgress DB instalations.**

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
        …
    ]

Posting
=======

You can add post messages in the admin interface now. Search for the label ``Aldryn_Blog``.

In order to display them, create a CMS page and install the app there (choose ``Blog`` from the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS site has become a blog post archive view.


Available CMS Plug-ins
======================

* ``Latest Blog Entries`` plugin lets you list **n** most frequent blog entries filtered by tags.
* ``Blog Authors`` plugin lists blog authors and the number of posts they have authored.
* ``Tags`` plugin lists the tags applied to all posts and allows filtering by these tags.
