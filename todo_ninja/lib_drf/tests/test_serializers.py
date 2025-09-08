from rest_framework.test import APITestCase
from books.models import Author, Book
from lib_drf.serializers import AuthorSerializer, BookSerializer


class SerializerTests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='Jhon', last_name='Doe', birth_date='1990-01-01')
        self.book = Book.objects.create(title='TestBook', author=self.author, published_date='2022-01-01', price=2.25)

    def test_author_serializer(self):
        serializer = AuthorSerializer(instance=self.author)
        self.assertEqual(serializer.data['first_name'], 'Jhon')

        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'birth_date': '1990-01-01'
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        author = serializer.save()
        self.assertEqual(author.first_name, 'Jane')

    def test_book_serializer(self):
        serializer = BookSerializer(instance=self.book)
        self.assertEqual(serializer.data['title'], 'TestBook')
        self.assertEqual(serializer.data['author']['last_name'], 'Doe')

        data = {
            'title': 'TestBook2',
            'published_date': '2025-08-19',
            'price': 2.0,
        }
        valid_data = data.copy()
        valid_data['author_id'] = self.author.pk
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.author, self.author)

        invalid_data = data.copy()
        invalid_data['author'] = self.author.pk
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
