from django.db import models

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
