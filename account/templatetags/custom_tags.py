from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if not isinstance(dictionary, dict):
        return None  # или возвращайте какое-либо другое значение по умолчанию
    return dictionary.get(key, [])


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter(name='get_other_participant_username')
def get_other_participant_username(room, user):
    other_participant = room.get_other_participant(user)
    return other_participant.username if other_participant else ""

