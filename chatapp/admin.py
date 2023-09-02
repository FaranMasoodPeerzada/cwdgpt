from django.contrib import admin
from .models import Registeration, Admin

from .models import Conversation, Message

# Register your models here.

admin.site.register(Registeration)


admin.site.register(Admin)


admin.site.register(Conversation)

admin.site.register(Message)
