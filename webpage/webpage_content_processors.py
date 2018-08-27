from django.conf import settings


def installed_apps(request):
    return {'APPS': settings.INSTALLED_APPS}
