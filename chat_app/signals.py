from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from LoveTouch.sqs_utils import send_message_to_sqs

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, **kwargs):
    """
    Отправляет уведомление в SQS каждый раз, когда создается новое сообщение.
    """
    message_data = {
        "room_id": instance.room.id,
        "sender_id": instance.sender.id,
        "content": instance.content
    }
    send_message_to_sqs(message_data)
