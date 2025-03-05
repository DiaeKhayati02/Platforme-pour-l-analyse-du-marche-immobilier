from django import template
from myapp.models import Message

register = template.Library()

@register.simple_tag
def inbox_count(user):
    return Message.objects.filter(receiver=user, is_read=False).count()

