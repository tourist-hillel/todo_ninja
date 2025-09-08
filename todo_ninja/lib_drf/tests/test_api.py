from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from books.models import Author, Book
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class DRFViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@mixins.com', password='password')
        self.token = Token.objects.create(user=self.user)
        self.author = Author.objects.create(
            first_name='Jhon', last_name='Doe', birth_date='1990-01-01'
        )
        self.available_book = Book.objects.create(
            title='AvailableBook',
            author=self.author,
            published_date='2022-01-01',
            price=2.25,
            is_available=True
        )

        self.book = Book.objects.create(
            title='TestBook',
            author=self.author,
            published_date='2022-01-01',
            price=2.25,
            is_available=False
        )

    def test_author_viewset(self):
        url = reverse('author-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url + '?last_name=Doe')
        self.assertEqual(len(response.data), 1)
        response = self.client.get(url + '?last_name=Smith')
        self.assertEqual(len(response.data), 0)

        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'birth_date': '1990-01-01'
        }
        url = reverse('author-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.filter(first_name='Jane', last_name='Smith').exists())

    def test_book_viewset(self):
        url = reverse('book-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        response = self.client.get(url + '?title=AvailableBook')
        self.assertEqual(len(response.data), 1)
        response = self.client.get(url + '?title=TestBook')
        self.assertEqual(len(response.data), 0)

        detail_url = reverse('book-detail', args=[self.available_book.pk])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.available_book.refresh_from_db()
        self.assertFalse(self.available_book.is_available)

        self.available_book.is_available = True
        self.available_book.save()
        response = self.client.delete(detail_url + '?mode=hard')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.available_book.pk).exists())
