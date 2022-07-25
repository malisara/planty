from django.db import models
from posts.models import Post
from users.models import User
from django.utils import timezone


class Chat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    message_reply = models.CharField(max_length=250)
    read_message_buyer = models.BooleanField(default=True)
    read_message_seller = models.BooleanField(
        default=True)
    date = models.DateTimeField(default=timezone.now)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
