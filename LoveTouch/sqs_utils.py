import boto3
import json

# Инициализация SQS клиента
sqs = boto3.client('sqs')
QUEUE_URL = 'https://sqs.eu-west-2.amazonaws.com/158135014313/LoveTouch'  # Замените на URL вашей SQS очереди

def send_message_to_sqs(chat_message):
    """
    Отправляет сообщение чата в SQS очередь.
    
    chat_message: dict
        Словарь содержащий информацию о сообщении, например:
        {
            "room_id": 123,
            "sender_id": 456,
            "content": "Привет, мир!"
        }
    """
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(chat_message)
    )
    return response

def poll_sqs_for_messages():
    """
    Опрашивает SQS на предмет новых сообщений.
    
    Возвращает список сообщений или пустой список, если сообщений нет.
    """
    messages = []
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,  # Максимальное количество сообщений для получения (макс. 10)
        WaitTimeSeconds=20  # Максимальное время ожидания (до 20 секунд)
    )
    
    if 'Messages' in response:
        messages = response['Messages']
        for message in messages:
            # Удаляем сообщение из очереди после его получения
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
    return messages

