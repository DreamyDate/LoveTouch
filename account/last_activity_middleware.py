from datetime import timedelta
from django.utils import timezone

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                if profile.last_activity is None:
                    profile.last_activity = timezone.now()
                    profile.save()
                else:
                    last_activity_age = timezone.now() - profile.last_activity
                    # Обновляем last_activity, если с последней активности прошло более 5 минут
                    if last_activity_age > timedelta(minutes=5):
                        profile.last_activity = timezone.now()
                        profile.save()

        response = self.get_response(request)
        return response
