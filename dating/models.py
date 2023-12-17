from django.db import models
from django.contrib.auth.models import User
from account.models import Profile


class Match(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='initiated_matches')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_matches')
    score = models.PositiveIntegerField()
    matched_on = models.DateTimeField(auto_now_add=True)
    is_confirmed_by_user1 = models.BooleanField(default=False)
    is_confirmed_by_user2 = models.BooleanField(default=False)

    def __str__(self):
        return f'Match between {self.user1.user.username} and {self.user2.user.username}'