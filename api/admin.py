from django.contrib import admin
from .models import Mailing, Client, Message
# Register your models here.

admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)
# admin.site.register(Project)