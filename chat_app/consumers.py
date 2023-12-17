import re
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Message, Room
from django.core.files.base import ContentFile
from io import BytesIO
import base64


@database_sync_to_async
def get_user_avatar_url(sender_id):
    try:
        user = User.objects.get(pk=sender_id)
        if user.profile.photo:
            return user.profile.photo.url
        else:
            return "/static/images/affect.jpg"  # Замените на свой путь к аватару по умолчанию
    except User.DoesNotExist:
        return "/static/images/affect.jpg"  # Замените на свой путь к аватару по умолчанию


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if 'message' in data:
            message = data['message']
            sender_id = data['sender_id']
            avatar_url = await get_user_avatar_url(sender_id)

            message = process_smilies(message)

            await self.save_message_to_db(message, sender_id)

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'avatar_url': avatar_url,
                'file_type': '1233',  # Отправляем тип файла для клиентской обработки

            })

        elif 'file' in data:  # Обработка файлов
            file_data = data['file']
            sender_id = data['sender_id']
            # Получите тип файла для обработки на стороне сервера
            file_type = data['file_type']
            file_name = data['file_name']
            avatar_url = await get_user_avatar_url(sender_id)

        # Обработка и сохранение файла, отправка его всем пользователям в чате и т.д.

            await self.process_and_send_file(file_data, file_type, sender_id)

            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': file_name,  # Отправляем URL файла
                'file_type': file_type,  # Отправляем тип файла для клиентской обработки
                'sender_id': sender_id,
                'avatar_url': avatar_url,


            })
            print("File type:", file_type)  # Логирование значения file_type

    @database_sync_to_async
    def process_and_send_file(self, file_data, file_type, sender_id):
        # Распаковываем данные файла и обрабатываем их
        file_content = base64.b64decode(file_data)
        # Имя файла с уникальным идентификатором отправителя
        file_name = f"file_{sender_id}.jpeg"

        try:
            room = Room.objects.get(pk=self.room_name)
            sender = User.objects.get(pk=sender_id)

            # Сохраняем файл в объекте сообщения (Message)
            message = Message.objects.create(
                room=room,
                sender=sender,
                # При необходимости можно добавить текстовое описание файла
                content=f'File: {file_name}',
            )

            # Определяем поле файла в зависимости от типа файла (изображение, документ и т.д.)
            if file_type == 'image/jpeg':
                message.image.save(file_name, ContentFile(file_content))
            elif file_type == 'document':
                message.document.save(file_name, ContentFile(file_content))
            elif file_type == 'gift':
                message.gift.save(file_name, ContentFile(file_content))
        except User.DoesNotExist:
            print("User does not exist.")
        except Room.DoesNotExist:
            print("Room does not exist.")
        except Exception as e:
            print(f"Exception occurred: {e}")

    @database_sync_to_async
    def save_message_to_db(self, message_content, sender_id):
        try:
            room = Room.objects.get(pk=self.room_name)
            sender = User.objects.get(pk=sender_id)

            message = Message.objects.create(
                room=room,
                sender=sender,
                content=message_content
            )
        except User.DoesNotExist:
            print("User does not exist.")
        except Room.DoesNotExist:
            print("Room does not exist.")

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        avatar_url = event['avatar_url']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'avatar_url': avatar_url
        }))


def process_smilies(message):
    smilies = {
        ':smiley1:': '😊',
        ':smiley2:': '😀',
        ':smiley3:': '😆',
        ':smiley4:': '😅',
        ':smiley5:': '🤣',
        ':smiley6:': '😂',
        ':smiley7:': '🙃',
        ':smiley8:': '😉',
        ':smiley9:': '😊',
        ':smiley10:': '😇',
        ':smiley11:': '🥰',
        ':smiley12:': '😍',
        ':smiley13:': '🤩',
        ':smiley14:': '😘',
        ':smiley15:': '😗',
        ':smiley16:': '😚',
        ':smiley17:': '😙',
        ':smiley18:': '😋',
        ':smiley19:': '😛',
        ':smiley20:': '😜',
        ':smiley21:': '🤪',
        ':smiley22:': '😝',
        ':smiley23:': '🤑',
        ':smiley24:': '🤗',
        ':smiley25:': '🤭',
        ':smiley26:': '🤫',
        ':smiley27:': '🤔',
        ':smiley28:': '🤐',
        ':smiley29:': '🤨',
        ':smiley30:': '😐',
        ':smiley31:': '😑',
        ':smiley32:': '😒',
        ':smiley33:': '🙄',
        ':smiley34:': '😮‍💨',
        ':smiley35:': '😔',
        ':smiley36:': '😪',
        ':smiley37:': '🤤',
        ':smiley38:': '😴',
        ':smiley39:': '😷',
        ':smiley40:': '🤒',
        ':smiley41:': '🤢',
        ':smiley42:': '🤮',
        ':smiley43:': '🥴',
        ':smiley44:': '😵',
        ':smiley45:': '😵‍💫',
        ':smiley46:': '🤯',
        ':smiley47:': '🤠',
        ':smiley48:': '🥳',
        ':smiley49:': '😎',
        ':smiley50:': '🤓',
        ':smiley51:': '🧐',
        ':smiley52:': '😕',
        ':smiley53:': '😟',
        ':smiley54:': '🙁',
        ':smiley55:': '☹️',
        ':smiley56:': '😲',
        ':smiley57:': '😳',
        ':smiley58:': '🥺',
        ':smiley59:': '😢',
        ':smiley60:': '😭',
        ':smiley61:': '😱',
        ':smiley62:': '😖',
        ':smiley63:': '🥱',
        ':smiley64:': '😤',
        ':smiley65:': '😡',
        ':smiley66:': '😠',
        ':smiley67:': '🤬',
        ':smiley68:': '😈',
        ':smiley69:': '👿',
        ':smiley70:': '💀',
        ':smiley71:': '☠️',
        ':smiley72:': '💩',
        ':smiley73:': '💋',
        ':smiley74:': '💯',
        ':smiley75:': '💦',
        ':smiley76:': '💌',
        ':smiley77:': '💘',
        ':smiley78:': '💝',
        ':smiley79:': '💖',
        ':smiley80:': '💞',
        ':smiley81:': '❣️',
        ':smiley82:': '💔',
        ':smiley83:': '❤️‍🔥',
        ':smiley84:': '🥂',
        ':smiley85:': '🍷 ',
        ':smiley86:': '🍸',

        # Добавьте другие смайлики
    }

    # Регулярное выражение для поиска смайлик-команд
    pattern = re.compile(r'(:\w+:)')
    message_with_images = pattern.sub(lambda match: smilies.get(
        match.group(0), match.group(0)), message)

    return message_with_images
