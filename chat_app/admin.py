from django.contrib import admin
from .models import Room, Message

from django.contrib.admin.widgets import FilteredSelectMultiple

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_private', 'is_archived', 'created_at')
    list_filter = ('is_private', 'is_archived')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'content', 'is_pinned', 'timestamp')
    list_filter = ('is_pinned', 'timestamp')

