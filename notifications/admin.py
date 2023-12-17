from django.contrib import admin
from .models import UserChannel, Notification

# Регистрация модели UserChannel
@admin.register(UserChannel)
class UserChannelAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel_name')
    search_fields = ('user__username', 'channel_name')

# Регистрация модели Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'message', 'is_read', 'timestamp')
    search_fields = ('recipient__username', 'sender__username', 'message')
    list_filter = ('is_read',)
