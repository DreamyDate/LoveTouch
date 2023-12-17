from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import UserChannel, Notification
import json
from account.models import Profile
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
        
    async def connect(self):
        self.user_id = str(self.scope["user"].id)
        
        # Подписываемся на группу
        await self.channel_layer.group_add(f"user_{self.user_id}", self.channel_name)
        
        # Сохраните channel_name для этого пользователя в базе данных
        await self.save_user_channel()

        await self.accept()

    async def disconnect(self, close_code):
        # Отписываемся от группы
        await self.channel_layer.group_discard(f"user_{self.user_id}", self.channel_name)
        
        # Удалите запись из базы данных при отключении пользователя.
        await self.delete_user_channel()

    @database_sync_to_async
    def save_user_channel(self):
        user_channel, created = UserChannel.objects.get_or_create(user_id=self.user_id)
        user_channel.channel_name = self.channel_name
        user_channel.save()

    @database_sync_to_async
    def delete_user_channel(self):
        try:
            user_channel = UserChannel.objects.get(user_id=self.user_id)
            user_channel.delete()
        except UserChannel.DoesNotExist:
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = data['recipient_id']
        notification_type = data['notification_type']

        sender = self.scope["user"]
        sender_name = sender.get_full_name() or sender.username

        # Получить аватарку отправителя
        sender_profile = await self.get_sender_profile(sender.id)
        sender_avatar_url = sender_profile.photo.url if sender_profile and sender_profile.photo else None
        
        await self.create_notification(sender, recipient_id, message)

        await self.channel_layer.group_send(
            
            f"user_{recipient_id}",
            {
                'type': 'send_notification',
                'message': message,
                'sender_name': sender_name,
                'sender_avatar_url': sender_avatar_url,
                'notification_type': notification_type,
            }
        )


    @database_sync_to_async
    def create_notification(self, sender, recipient_id, message):
        recipient = User.objects.get(pk=recipient_id)
        Notification.objects.create(recipient=recipient, sender=sender, message=message)
    
    @sync_to_async
    def find_user(self, full_name):
        try:
            first_name, last_name = full_name.split()  # Предполагается, что имя и фамилия разделены пробелом
            # Ищем пользователя по комбинации имени и фамилии
            return User.objects.get(first_name=first_name, last_name=last_name)
        except User.DoesNotExist:
            return None  # Возвращаем None, если пользователь не найден
        except Exception as e:
            print(f"Error finding user: {e}")  # Обработка других исключений, если таковые возникнут
            return None


    async def send_notification(self, event):
       
        notification_type = event.get('notification_type', 'default')  # Получаем тип уведомления или используем 'default', если тип не указан

        if notification_type == 'birthdays':
            await self.send_birthdays_notification(event)
        elif notification_type == 'gift':
            await self.send_gift(event)
        elif notification_type == 'acquaintance':
            await self.send_acquaintance(event)
        elif notification_type == 'other':
            await self.send_other(event)

        else:
            # Обработка уведомлений с неизвестным типом или типом 'default'
            await self.send_default_notification(event)

# Пример обработки уведомления типа 'message'
    async def send_birthdays_notification(self, event):
        await self.send(text_data=json.dumps({
        'notification_type': 'birthdays',
        'message': event['message'],
        'sender_name': event['sender_name'],
        'sender_avatar_url': event['sender_avatar_url'],
    }))
        

# Пример обработки уведомления другого типа ('gift')
    async def send_gift(self, event):
    # Обработка уведомления типа "gift"
        await self.send(text_data=json.dumps({
        'notification_type': 'gift',
        'message': event['message'],
        'sender_name': event['sender_name'],
        'sender_avatar_url': event['sender_avatar_url'],
    }))

        sender = await self.find_user(event['sender_name'])
        recipient_id = event['recipient_id']
        message = event['message']
        await self.create_notification(sender, recipient_id, message)

# Пример обработки уведомления другого типа ('acquaintance')
    async def send_acquaintance(self, event):
    # Обработка уведомления типа "acquaintance"
        await self.send(text_data=json.dumps({
        'notification_type': 'acquaintance',
        'message': event['message'],
        'sender_name': event['sender_name'],
        'sender_avatar_url': event['sender_avatar_url'],
    }))
        sender = await self.find_user(event['sender_name'])

        recipient_id = event['recipient_id']
        message = event['message']
        await self.create_notification(sender, recipient_id, message)


# Пример обработки уведомления другого типа ('gift')

    async def send_other(self, event):
        # Обработка уведомления типа "gift"
        await self.send(text_data=json.dumps({
            'notification_type': 'other',
            'message': event['message'],
            'sender_name': event['sender_name'],
            'sender_avatar_url': event['sender_avatar_url'],
        }))

        sender = await self.find_user(event['sender_name'])
        recipient_id = event['recipient_id']
        message = event['message']
        await self.create_notification(sender, recipient_id, message)


# Обработка уведомлений с неизвестным типом или типом 'default'
    async def send_default_notification(self, event):
        await self.send(text_data=json.dumps({
        'notification_type': 'default',
        'message': event['message'],
        'sender_name': event['sender_name'],
        'sender_avatar_url': event['sender_avatar_url'],
    }))
        # Вызываем create_notification с использованием database_sync_to_async
        await database_sync_to_async(self.create_notification)(
            sender=self.scope["user"],
            recipient_id=event["recipient_id"],
            message=event["message"]
        )
        


    @database_sync_to_async
    def get_sender_profile(self, user_id):
        try:
            return Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return None
