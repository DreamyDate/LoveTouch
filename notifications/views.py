from django.http import JsonResponse
from .models import Notification
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def read_notification(request, notification_id):
    if request.method == "POST":
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({"status": "success"})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notification not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Bad request method"}, status=400)


from django.http import JsonResponse

@csrf_exempt
@login_required
def read_all_notifications(request):
    if request.method == "POST":
        try:
            # Помечаем все уведомления пользователя как прочитанные
            Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
            return JsonResponse({"status": "success"})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notifications not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Bad request method"}, status=400)
