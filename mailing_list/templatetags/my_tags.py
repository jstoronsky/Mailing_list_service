from django import template
register = template.Library()


@register.filter()
def mediapath(value):
    if value:
        return f'/media/{value}'
    return ''


@register.simple_tag()
def mediapath(value):
    if value:
        return f'/media/{value}'
    return ""
