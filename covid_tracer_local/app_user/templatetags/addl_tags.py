# additional custom tags for this app

from django import template

from datetime import datetime, timedelta

register = template.Library()

@register.simple_tag
def past3day():
    """Returns (today - 3 days) date"""
    past_date = datetime.today() - timedelta(days=7)
    return past_date.strftime("%d-%m-%Y")