from django.core.management.base import BaseCommand
from LoveTouch.sqs_utils import poll_sqs_for_messages

class Command(BaseCommand):
    help = "Опрашивает SQS на предмет новых сообщений."

    def handle(self, *args, **options):
        messages = poll_sqs_for_messages()
        for message in messages:
            # Обработайте каждое сообщение как вам нужно. Например, можете записывать их в базу данных.
            pass
