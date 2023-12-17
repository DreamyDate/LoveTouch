from django.conf import settings
from django.db import models
from django.utils import timezone


class Room(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_private = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first()
        
    def get_unread_messages_count(self, user):
        return self.messages.exclude(messagereadstatus__user=user, messagereadstatus__read_at__isnull=False).count()
    def get_last_message(self):
        return self.messages.order_by('-timestamp').first()


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    
    is_pinned = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Добавляем поле для отслеживания прочтения

    # Новые поля для различных типов файлов
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    document = models.FileField(upload_to='chat_documents/', null=True, blank=True)
    gift = models.FileField(upload_to='chat_gifts/', null=True, blank=True)
    # Добавьте поля для других типов файлов, если необходимо

    def mark_as_read(self, user):
        if user != self.sender:
            self.is_read = True
            self.save()

   
