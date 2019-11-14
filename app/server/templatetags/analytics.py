from django import template

from app import settings

register = template.Library()


@register.inclusion_tag('tags/google_analytics.html')
def google_analytics():
    return {'google_tracking_id': settings.GOOGLE_TRACKING_ID}


@register.inclusion_tag('tags/azure_appinsights.html')
def azure_appinsights():
    return {
        'DEBUG': settings.DEBUG,
        'azure_appinsights_ikey': settings.APPLICATION_INSIGHTS['ikey'],
        'azure_appinsights_endpoint': settings.APPLICATION_INSIGHTS['endpoint'],
    }
