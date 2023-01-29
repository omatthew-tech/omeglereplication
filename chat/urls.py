from django.urls import path
from .views import index, room
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('live_stream/', views.live_stream, name='live_stream'),
]
