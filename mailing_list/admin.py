from django.contrib import admin
from mailing_list.models import Client, Message, Logs, CustomInterval
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'email', 'commentary')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'body', 'time_to_start', 'time_to_end', 'status')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('message', 'datetime_of_attempt', 'status')


@admin.register(CustomInterval)
class CustomIntervalAdmin(admin.ModelAdmin):
    list_display = ('message', 'period', 'every')
