from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_folder_products')
def media_folder_products(string):

    if not string:
        return '/static/img/not-available.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):

    if not string:
        string = 'avatar-default.jpg'

    return f'{settings.MEDIA_URL}{string}'

