from django.conf import settings


def installed_apps(request):
    return {'APPS': settings.INSTALLED_APPS}


def is_dev_version(request):
    try:
        return {'DEV_VERSION': settings.DEV_VERSION}
    except AttributeError:
        return {}
