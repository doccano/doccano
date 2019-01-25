from django import template

from app import settings

register = template.Library()


@register.inclusion_tag('tags/google_analytics.html')
def google_analytics():
    return {'google_tracking_id': settings.GOOGLE_TRACKING_ID}
