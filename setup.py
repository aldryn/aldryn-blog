# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_blog import __version__

REQUIREMENTS = [
    'django-taggit<0.12',
    'django-filer',
    'django_select2',
    'djangocms-text-ckeditor',
    'django-appconf',
    'django-classy-tags',
    'south>=0.8',
    'aldryn_common',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-blog',
    version=__version__,
    description='Adds blogging abilities to django CMS',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-blog',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
