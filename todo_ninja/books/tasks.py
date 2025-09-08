import os
import json
from celery import shared_task
from django.conf import settings
from datetime import datetime
from books.models import Book, Author


@shared_task
def notify_new_book(book_id):
    try:
        book = Book.objects.get(id=book_id)
        stats = {
            'book_id': book_id,
            'title': book.title,
            'author': str(book.author),
            'published_date': str(book.published_date),
            'price': str(book.price),
            'is_available': book.is_available,
            'added_at': str(datetime.now().isoformat())
        }
        output_path = os.path.join(settings.MEDIA_ROOT, 'statistics', f'book_{book_id}.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
    except Book.DoesNotExist:
        pass

@shared_task
def generate_book_report():
    books = Book.objects.all()
    report_context = {
        'total_books': books.count(),
        'books': [
            {
                'id': book.id,
                'title': book.title,
                'author': str(book.author),
                'published_date': str(book.published_date),
                'price': str(book.price),
                'is_available': book.is_available,
            } for book in books
        ],
        'generated_at': str(datetime.now().isoformat())
    }
    output_path = os.path.join(settings.MEDIA_ROOT, 'statistics', f'book_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_context, f, indent=4, ensure_ascii=False)
