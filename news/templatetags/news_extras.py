from django import template
from news.models import NewsFeed

register = template.Library()


@register.inclusion_tag('news/newsfeed.html')
def newsfeed(amount=None):
    if amount is None:
        feeds = NewsFeed.objects.all()
    else:
        feeds = NewsFeed.objects.all()[0:amount]
    return {'feeds': feeds}


@register.inclusion_tag('news/newsfeed_bootstrap_panel.html')
def newsfeed_bootstrap_panel(amount=None):
    if amount is None:
        feeds = NewsFeed.objects.all()
    else:
        feeds = NewsFeed.objects.all()[0:amount]
    return {'feeds': feeds}


@register.inclusion_tag('news/newsfeed_list.html')
def newsfeed_list(amount=None):
    if amount is None:
        feeds = NewsFeed.objects.all()
    else:
        feeds = NewsFeed.objects.all()[0:amount]
    return {'feeds': feeds}


@register.inclusion_tag('news/newsfeed_table.html')
def newsfeed_table(amount=None):
    if amount is None:
        feeds = NewsFeed.objects.all()
    else:
        feeds = NewsFeed.objects.all()[0:amount]
    return {'feeds': feeds}


@register.inclusion_tag('news/newsfeed.html')
def newsfeed_last_items(amount=None):
    if amount is None:
        feeds = NewsFeed.objects.all()
    else:
        feeds = NewsFeed.objects.all()[0:amount]
    return {'feeds': feeds}
