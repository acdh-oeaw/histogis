from django import template
from webpage.metadata import PROJECT_METADATA as PM

register = template.Library()


@register.simple_tag
def projects_metadata(key):
    return PM[key]


@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    inspired by https://stackoverflow.com/questions/14496978/fields-verbose-name-in-templates
    call in template like e.g. 'get_verbose_name <classname> "<fieldname>" '
    """
    try:
        label = instance._meta.get_field(field_name).verbose_name
    except:
        label = None
    if label:
        return "{}".format(label)
    else:
        return "No verbose name for '{}' provided".format(field_name)


@register.simple_tag
def get_help_text(instance, field_name):
    """
    Returns help_text for a field.
    inspired by https://stackoverflow.com/questions/14496978/fields-verbose-name-in-templates
    call in template like e.g.  get_help_text <classname> "<fieldname>"
    """
    try:
        label = instance._meta.get_field(field_name).help_text
    except:
        label = None
    if label:
        return "{}".format(label)
    else:
        return "No helptext for '{}' provided".format(field_name)
