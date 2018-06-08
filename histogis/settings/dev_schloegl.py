from .base import *

SPARQL_ENDPOINT = 'https://bgdefc.eos.arz.oeaw.ac.at/sparql'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^mm-24*i-6iecm7c@z9l+7%^ns^4g^z!8=dgffg4ulggr-4=1%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += ('django_extensions',)

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'histogis',
        'USER': 'histogis',
        'PASSWORD': 'yH1Oxk2SCv1Z',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
