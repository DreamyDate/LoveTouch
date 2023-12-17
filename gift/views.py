from django.shortcuts import render, get_object_or_404, redirect
from .models import GiftItem, GiftPurchase, GiftCategory
from django.contrib.auth.models import User
from account.models import CreditTransaction, Profile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages

def gift_shop(request):
    gifts = GiftItem.objects.all()
    categories = GiftCategory.objects.all()
    new_gifts = GiftItem.objects.filter(is_new=True)
    return render(request, 'gift_shop.html', {'gifts': gifts, 'categories': categories, 'new_gifts': new_gifts})

def buy_gift(request, gift_id):
    gift = get_object_or_404(GiftItem, id=gift_id)
    user = request.user

    # Инициализируем friends пустым списком
    friends = []
    current_user_profile = Profile.objects.get(user=request.user)
    # Проверяем, есть ли текущий пользователь и имеет ли он друзей
    if current_user_profile:
        friends = current_user_profile.friends.all()

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, id=recipient_id)

        profile = Profile.objects.get(user=user)

        current_balance = calculate_user_balance(user)
        
   
        if current_balance < gift.price:
            messages.error(request, "Insufficient funds to purchase the gift")
            return redirect('buy_gift', gift_id=gift_id)  # Перенаправление обратно на страницу покупки подарка

        GiftPurchase.objects.create(buyer=user, recipient=recipient, gift_item=gift)

        profile.credits -= gift.price
        profile.save()

        create_credit_transaction(user, -gift.price, f"Purchase of {gift.name}")
            
        avatar_url = user.profile.photo.url
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"user_{recipient_id}", {
            'type': 'send_notification',
            'message': f"You received a gift:'{gift.name}'. You can see the gift in your profile",
            'recipient_id': recipient_id,
            'notification_type': 'gift',
            'sender_name': user.get_full_name() or user.username,
            'sender_avatar_url': avatar_url,
        })
        return redirect('buy_gift', gift_id=gift_id)

    # Your remaining code for handling GET requests and rendering the buy_gift page goes here

    return render(request, 'buy_gift.html', {'gift': gift, 'friends': friends})


def calculate_user_balance(user):
    try:
        profile = Profile.objects.get(user=user)
        # Получаем все транзакции пользователя
        transactions = CreditTransaction.objects.filter(user=profile)
        # Рассчитываем текущий баланс
        balance = profile.credits
        
        return balance
    except Profile.DoesNotExist:
        return 0  # Если профиль не найден, баланс равен 0

def create_credit_transaction(user, amount, description):
    try:
        profile = Profile.objects.get(user=user)
        # Создаем запись о транзакции
        transaction = CreditTransaction.objects.create(
            user=profile,
            amount=amount,
            transaction_type='C' if amount > 0 else 'D',
            description=description
        )
        return transaction
    except Profile.DoesNotExist:
        return None  # Если профиль не найден, возвращаем None



def gift_purchase_success(request):
    if request.META.get('HTTP_REFERER'):
        return redirect(request.META['HTTP_REFERER'])
    else:
        # Если HTTP_REFERER отсутствует, выполните какой-либо другой код или перенаправьте на другую страницу
        return render(request, 'gift_purchase_success.html')
