from django.contrib import admin
from mailing_list.models import Client, Message, Logs, SettingsMailing
# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'middle_name', 'email', 'commentary')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'body')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('message', 'datetime_of_attempt', 'status')


@admin.register(SettingsMailing)
class SettingslAdmin(admin.ModelAdmin):
    list_display = ('message', 'period', 'every', 'time_to_start', 'time_to_end', 'status')
