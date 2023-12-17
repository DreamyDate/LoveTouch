from .models import PremiumPurchase
from notifications.models import Notification
from chat_app.models import Room, Message
from .models import MenuItem
from pages.models import Page
from chat_app.utils.message_utils import count_total_unread_messages
from django.db.models import Max


def menu(request):
    menu_items = MenuItem.objects.filter(enabled=True)
    return {'menu_items': menu_items}

def referer(request):
    return {'referer': request.META.get('HTTP_REFERER', 'your_default_url')}


def footer_menu(request):
    pages_in_footer = Page.objects.filter(show_in_footer=True)
    return {'footer_pages': pages_in_footer}


def global_context(request):
    is_premium = False
    unread_count = 0
    latest_messages = []
    total_unread_count = 0
    unread_notifications = []
   
    # Проверка наличия записи о премиум-покупке для профиля пользователя
    if request.user.is_authenticated:
        try:
            premium_purchase = PremiumPurchase.objects.get(
                profile=request.user.profile)
            if premium_purchase:
                is_premium = True
        except PremiumPurchase.DoesNotExist:
            pass

        # Подсчет непрочитанных уведомлений
        unread_notifications = Notification.objects.filter(
            recipient=request.user, is_read=False)
        unread_count = unread_notifications.count()

        # Получение последних сообщений в чатах пользователя
        latest_messages = Room.objects.filter(participants=request.user)
        latest_messages = latest_messages.annotate(
            last_message_timestamp=Max('messages__timestamp'))
        latest_messages = latest_messages.order_by('-last_message_timestamp')

        # Подсчет общего числа непрочитанных сообщений в чатах пользователя
        total_unread_count = count_total_unread_messages(request.user)

    return {
        'is_premium': is_premium,
        'unread_count': unread_count,
        'notifications': unread_notifications,
        'latest_messages': latest_messages,
        'total_unread_count': total_unread_count,
        
    }
