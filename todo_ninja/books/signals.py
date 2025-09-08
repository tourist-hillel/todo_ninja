from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal
from books.models import Book, Messages, UploadedFiles


file_word_count = Signal()

class MessageContextProcessor:
    _messages = []

    @classmethod
    def add_message(cls, level, message):
        cls._messages.append({'level': level, 'message': message})

    @classmethod
    def get_messages(cls):
        messages = cls._messages
        cls._messages.clear()
        return messages
    
    @classmethod
    def upload_to_model(cls):
        for message in cls._messages:
            Messages.objects.create(message=message['message'])
        cls._messages.clear()
    
    

@receiver(pre_save, sender=Book)
def capture_old_price(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Book.objects.get(pk=instance.pk)
            new_price = instance.price
            old_price = old_instance.price
            MessageContextProcessor.add_message(
                level='success',
                message=f'Для книги {instance.title} знмінилась ціна з {old_price} на {new_price}'
            )
            MessageContextProcessor.upload_to_model()
        except Book.DoesNotExist:
            pass
    else:
        MessageContextProcessor.add_message(
            level='success',
            message=f'Для книги {instance.title} встановлена ціна {instance.price}'
        )
        MessageContextProcessor.upload_to_model()


@receiver(file_word_count, sender=UploadedFiles)
def check_word_count(sender, instance, word_limit, **kwargs):
    if instance.word_count > word_limit:
        MessageContextProcessor.add_message(
            level='warning',
            message=f'Для файлу {instance.filename} перевищено ліміт символів. Максимальний поточний ліміт: {word_limit}'
        )
        MessageContextProcessor.upload_to_model()
