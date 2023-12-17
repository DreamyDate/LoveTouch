from django.contrib import admin
from .models import Match

# ... Ваш класс ProfileAdmin ...

class MatchAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'score', 'matched_on']
    search_fields = ['user1__user__username', 'user2__user__username']
    list_filter = ['matched_on']
    date_hierarchy = 'matched_on'

admin.site.register(Match, MatchAdmin)

