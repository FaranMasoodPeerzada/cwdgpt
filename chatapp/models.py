from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Registeration(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name= models.CharField(max_length=255)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    user_email=models.EmailField(max_length=50)
    user_password=models.CharField(max_length= 255)
    def __str__(self):
        return self.user_name




from django.contrib.auth.models import User
import datetime
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    chat_title=models.TextField(default="My First Chat")
    document = models.FileField(upload_to='documents/', default='default_document.pdf')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.chat_title

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    text = models.TextField(default="hello")
    response = models.TextField(default="helo")
    is_user_message = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
















