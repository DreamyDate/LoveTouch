from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from account.models import Profile


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def chat_page(request):
    rooms = Room.objects.filter(participants=request.user, is_archived=False).prefetch_related('messages')
    friends_online = request.user.profile.friends_online()
    for room in rooms:
        last_message = room.messages.order_by('-timestamp').first()
        room.last_message_content = last_message.content if last_message else "No messages in this chat yet."
        room.last_message_timestamp = last_message.timestamp if last_message else "N/A"
        
        # Получаем "другого участника" чата
        room.other_participant = room.get_other_participant(request.user)
        room.other_participant_avatar = room.other_participant.profile.photo.url if room.other_participant.profile.photo else None

    context = {
        'rooms': rooms,
        'friends_online':friends_online,

    }

    return render(request, 'chat_app/chat_list.html', context)

from django.shortcuts import render, get_object_or_404

def chat_detail(request, room_id):
    # Получаем комнату по ID или возвращаем 404 ошибку, если комнаты с таким ID нет
    room = get_object_or_404(Room, id=room_id)
    
    # Убеждаемся, что пользователь является участником этой комнаты
    if request.user not in room.participants.all():
        # Вы можете обработать это иначе, например, вернуть ошибку или перенаправить
        return HttpResponseForbidden("You are not a participant of this chat.")
    
    messages = room.messages.order_by('timestamp')
    other_participant = room.get_other_participant(request.user)
    blocked_users = request.user.profile.blocked_users.values_list('id', flat=True)
    friends_online = request.user.profile.friends_online()
    context = {
        'room': room,
        'messages': messages,
        'other_participant': other_participant,
        'friends_online':friends_online,
        'blocked_users': blocked_users,  # Передаем список заблокированных пользователей в контекст
    }

    return render(request, 'chat_app/chat_detail.html', context)

@login_required
def create_chat(request):
    if request.method == "POST":
        friend_id = request.POST.get('friend_id')
        try:
            friend = User.objects.get(id=friend_id)

            # Проверка на заблокированного друга
            if request.user.profile.is_blocked_user(friend.profile):
                messages.error(request, 'Пользователь заблокирован и не может быть добавлен в чат.')
                return redirect('home')

            # Проверка на обратную блокировку
            if friend.profile.is_blocked_user(request.user.profile):
                messages.error(request, 'Вы не можете отправить сообщение этому пользователю.')
                return redirect('home')
            
            # Проверка на наличие чата между текущим пользователем и другом
            existing_chat = Room.objects.filter(participants=friend).filter(participants=request.user)
            if existing_chat.exists():
                messages.error(request, 'Чат с этим пользователем уже существует.')
                return redirect('home')
            
            new_chat = Room.objects.create()
            new_chat.participants.add(request.user)
            new_chat.participants.add(friend)
            new_chat.save()
            return redirect('chat:chat_page')

        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким ID не найден.')
            return redirect('home')

    return redirect('home')


@login_required
def block_user(request, user_id):  # Принимает user_id как часть URL
    user_to_block = get_object_or_404(Profile, id=user_id)
    current_user_profile = request.user.profile

    # Проверка, не заблокирован ли уже пользователь
    if current_user_profile.is_blocked_user(user_to_block):
        messages.warning(request, 'Пользователь уже заблокирован.')
        return JsonResponse({'error': 'Пользователь уже заблокирован.'}, status=400)

    # Блокировка пользователя
    current_user_profile.add_to_blacklist(user_to_block)
    messages.success(request, 'Пользователь успешно заблокирован.')
    return JsonResponse({'message': 'Пользователь успешно заблокирован.'})

@login_required
def unblock_user(request, user_id):  # Принимает user_id как часть URL
    user_to_unblock = get_object_or_404(Profile, id=user_id)
    current_user_profile = request.user.profile

    # Проверка, заблокирован ли уже пользователь
    if not current_user_profile.is_blocked_user(user_to_unblock):
        messages.warning(request, 'Пользователь не заблокирован.')
        return JsonResponse({'error': 'Пользователь не заблокирован.'}, status=400)

    # Разблокировка пользователя
    current_user_profile.remove_from_blacklist(user_to_unblock)
    messages.success(request, 'Пользователь успешно разблокирован.')
    return JsonResponse({'message': 'Пользователь успешно разблокирован.'})




def chat_ws(request, chat_id):
    # Здесь будет логика для веб-сокета чата
    pass


def delete_chat(request, chat_id):
    try:
        chat = get_object_or_404(Room, id=chat_id)
        chat.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # логирование ошибки
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user in message.room.participants.all():
        message.mark_as_read(request.user)
        return JsonResponse({'status': 'success', 'was_viewed': True})
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not a participant of this chat.'}, status=403)


@login_required
def latest_chats(request):
    rooms = Room.objects.filter(participants=request.user, is_archived=False).prefetch_related('messages')

    latest_chats = []
    for room in rooms:
        last_message = room.messages.order_by('-timestamp').first()
        last_message_content = last_message.content if last_message else "No messages in this chat yet."
        last_message_timestamp = last_message.timestamp if last_message else "N/A"
        other_participant = room.get_other_participant(request.user)
        other_participant_avatar = other_participant.profile.photo.url if other_participant.profile.photo else None

        latest_chats.append({
            'other_participant_name': other_participant.username,  # Имя другого участника
            'other_participant_avatar': other_participant_avatar,  # Аватар другого участника
            'last_message': last_message_content,  # Содержание последнего сообщения
            'last_message_time': last_message_timestamp,  # Время последнего сообщения
            'unread': True if last_message and not last_message.is_read(request.user) else False,  # Флаг непрочитанных сообщений
        })

    return JsonResponse(latest_chats, safe=False)
