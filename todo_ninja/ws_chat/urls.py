from django.urls import path
from ws_chat.views import index

urlpatterns = [
    path('room/<str:room_name>/', index, name='chat'),
]
