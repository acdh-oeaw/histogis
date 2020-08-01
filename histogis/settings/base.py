"""
Django settings for histogis project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, '../'))))

ACDH_IMPRINT_URL = "https://shared.acdh.oeaw.ac.at/acdh-common-assets/api/imprint.php?serviceID="

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'crispy_forms',
    'django_filters',
    'django_tables2',
    'rest_framework',
    'rest_framework_gis',
    'django_extensions',
    'leaflet',
    'idprovider',
    'webpage',
    'vocabs',
    'stats',
    'shps',
    'charts',
    'browsing',
    'news',
    'analyze',
    'archeutils',
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'

}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'histogis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webpage.webpage_content_processors.installed_apps',
                'webpage.webpage_content_processors.is_dev_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'histogis.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
TEMP_DIR = os.path.join(BASE_DIR, 'temp/')

ARCHE_SETTINGS = {
    'project_name': ROOT_URLCONF.split('.')[0],
    'base_url': "https://id.acdh.oeaw.ac.at/{}".format(ROOT_URLCONF.split('.')[0])
}

VOCABS_DEFAULT_PEFIX = os.path.basename(BASE_DIR)

VOCABS_SETTINGS = {
    'default_prefix': VOCABS_DEFAULT_PEFIX,
    'default_ns': "http://www.vocabs/{}/".format(VOCABS_DEFAULT_PEFIX),
    'default_lang': "eng"
}

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (47, 16),
    'DEFAULT_ZOOM': 6,
    'MIN_ZOOM': 3,
    'OVERLAYS': [
        (
            'dinamlex',
            'https://maps.acdh.oeaw.ac.at/mapserv?map=/data/test.map&mode=tile&layers=test&tilemode=gmap&tile={x}+{y}+{z}',
            {
                'maxZoom': 18,
                'opacity': 0.7
            }
        ),
        (
            'czoernig',
            'https://maps.acdh.oeaw.ac.at/mapserv?map=/data/czoernig.map&mode=tile&layers=czoernig&tilemode=gmap&tile={x}+{y}+{z}',
            {
                'maxZoom': 18,
                'opacity': 0.7
            }
        ),
        (
            'tirol',
            'https://maps.acdh.oeaw.ac.at/mapserv?map=/data/tirol.map&mode=tile&layers=tirol&tilemode=gmap&tile={x}+{y}+{z}',
            {
                'maxZoom': 18,
                'opacity': 0.7
            }
        ),
    ]
}

ARCHE_PROJECT_NAME = "HistoGIS"
ARCHE_BASE_URL = "https://id.acdh.oeaw.ac.at/histogis"
ARCHE_LANG = 'en'
ARCHE_PAYLOAD_MIMETYPE = 'application/geo+json'

ARCHE_CONST_MAPPINGS = [
    ('hasOwner', "https://d-nb.info/gnd/1123037736",),  # ACDHCH
    ('hasContact', "https://d-nb.info/gnd/1123037736",),
    ('hasRightsHolder', "https://d-nb.info/gnd/1123037736",),
    ('hasPrincipalInvestigator', "https://d-nb.info/gnd/1154715620",),
    ('hasPrincipalInvestigator', "https://d-nb.info/gnd/1043833846",),
    ('hasLicensor', 'https://d-nb.info/gnd/1123037736',),
    ('hasLicense', 'https://creativecommons.org/licenses/by/4.0/',),
    ('hasRelatedDiscipline', 'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601',),
    ('hasSubject', 'GIS',),
    ('hasSubject', 'Historic administrative units',),
    ('hasMetadataCreator', 'https://d-nb.info/gnd/1043833846',),  # pandorfer
    ('hasDepositor', 'https://d-nb.info/gnd/1043833846',),  # pandorfer
]
