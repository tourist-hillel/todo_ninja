from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from books.models import Author, Book
from lib_drf.serializers import AuthorSerializer, BookSerializer
from lib_drf.auth import LibJWTAuthentication
from books.tasks import notify_new_book

from rest_framework import status
from rest_framework.response import Response


class AuthorViewSet(viewsets.ModelViewSet):
    # permission_classses = []
    authentication_classes = [TokenAuthentication]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name']

class BookViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Book.objects.filter(is_available=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'published_date']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.query_params.get('mode') == 'hard':
            self.perform_destroy(instance)
        else:
            self.perform_soft_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_soft_destroy(self, instance):
        instance.is_available = False
        instance.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        book = serializer.instance
        notify_new_book.delay(book.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)
