from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='in_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='brutto')
def brutto(value):
    return round((float(value) * 0.23) + float(value), 2)
