from chat_app.models import Message
from django.db.models import Q

def count_total_unread_messages(user):
    total_unread_count = Message.objects.filter(
        room__participants=user,
        is_read=False
    ).exclude(sender=user).count()
    return total_unread_count
