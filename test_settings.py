HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'INSTALLED_APPS': [
        'taggit',
        'aldryn_blog',
        'easy_thumbnails',
        'filer',
        'djangocms_text_ckeditor',
        'django_select2',
        'aldryn_common',
        'hvad',
    ],
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
}
