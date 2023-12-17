from django.db import models
from django.conf import settings

class UserChannel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='other_notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

