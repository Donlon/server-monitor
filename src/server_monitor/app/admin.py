from django.contrib import admin

# Register your models here.

from .models import Client, Record

admin.site.register(Client)
admin.site.register(Record)
