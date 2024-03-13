from django.contrib import admin

from mailing.models import Mailing, Client, Log, Message

admin.site.register(Mailing)

admin.site.register(Client)

admin.site.register(Log)

admin.site.register(Message)