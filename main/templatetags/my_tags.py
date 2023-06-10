from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def mediapath(image_path):
    full_image_path = settings.MEDIA_URL + str(image_path)
    return full_image_path