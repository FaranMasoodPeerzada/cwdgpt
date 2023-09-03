from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.hashers import make_password

class Registeration(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name= models.CharField(max_length=255)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    user_email=models.EmailField(max_length=50)
    user_password=models.CharField(max_length= 255)
    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     self.user_password = make_password(self.user_password)
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.user_name
    def __str__(self):
        return self.user_name


class Admin(models.Model):
    
    admin_id = models.BigAutoField(primary_key=True)
    admin_name= models.CharField(max_length=255)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    admin_email=models.EmailField(max_length=50)
    admin_password=models.CharField(max_length= 255)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.admin_password = make_password(self.admin_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.admin_name


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
















