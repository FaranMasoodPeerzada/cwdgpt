from django.contrib import admin
from .models import Registeration

from .models import Conversation, Message

# Register your models here.

admin.site.register(Registeration)


admin.site.register(Conversation)

admin.site.register(Message)
