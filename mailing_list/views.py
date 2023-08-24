from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from mailing_list.forms import MessageAddForm, MessageUpdateForm, ClientAddForm, ClientUpdateForm, SettingsAddForm
from mailing_list.models import Client, Message, Logs, SettingsMailing
from blog.models import Blog
from django.forms import inlineformset_factory


# Create your views here.
class MailingHomepage(TemplateView):
    template_name = 'mailing_list/home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        blogs = Blog.objects.all()[:3]
        all_messages = len(Message.objects.all())
        active_messages = len(SettingsMailing.objects.filter(status='Идёт рассылка'))
        all_clients = len(Client.objects.all())
        context_data['blogs'] = blogs
        context_data['all_messages'] = all_messages
        context_data['active_messages'] = active_messages
        context_data['all_clients'] = all_clients
        return context_data


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Managers').exists():
            return queryset
        else:
            return queryset.filter(user=self.request.user)


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageAddForm
    success_url = reverse_lazy('mailing_list:message_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        interval_form_set = inlineformset_factory(Message, SettingsMailing, form=SettingsAddForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = interval_form_set(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = interval_form_set(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        object_ = form.save()
        if formset.is_valid():
            formset.instance = object_
            formset.save()
            message = object_
            current_time = timezone.now()
            if message.settingsmailing.time_to_start <= current_time:
                PeriodicTask.objects.create(name=f'mailing list_{message}', task=f'send_mail_{object_.pk}_to_clients',
                                            interval=SettingsMailing.objects.get(pk=message.pk,
                                                                                 every=message.settingsmailing.every,
                                                                                 period=message.settingsmailing.period),
                                            start_time=timezone.now(), expires=message.settingsmailing.time_to_end)
            elif message.settingsmailing.time_to_start > current_time:
                PeriodicTask.objects.create(name=f'mailing list_{message}', task=f'send_mail_{object_.pk}_to_clients',
                                            interval=SettingsMailing.objects.get(pk=message.pk,
                                                                                 every=message.settingsmailing.every,
                                                                                 period=message.settingsmailing.period),
                                            start_time=message.settingsmailing.time_to_start,
                                            expires=message.settingsmailing.time_to_end)
            with open('mailing_list/tasks.py', 'at') as tasks:
                function_code = f"""
@shared_task(name='send_mail_{message.pk}_to_clients')
def send_mail_to_{message.pk}_clients():
    clients = Client.objects.all()
    message = Message.objects.get(pk={message.pk})
    for client in clients:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, [client.email])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        message.settingsmailing.status = 'Идёт рассылка'
        message.settingsmailing.save(update_fields=['status'])
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_{message}_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'Завершена'
            message.settingsmailing.save(update_fields=['status']) 


"""
                tasks.write(function_code)
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageUpdateForm
    success_url = reverse_lazy('mailing_list:message_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        interval_form_set = inlineformset_factory(Message, SettingsMailing, form=SettingsAddForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = interval_form_set(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = interval_form_set(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        object_ = form.save()
        if formset.is_valid():
            formset.instance = object_
            formset.save()
            message = object_
            current_time = timezone.now()
            if message.settingsmailing.time_to_start <= current_time:
                PeriodicTask.objects.filter(name=f'mailing list_{message}').update(
                    name=f'mailing list_{message}', interval=IntervalSchedule.objects.get(
                        pk=message.pk,
                        every=message.settingsmailing.every,
                        period=message.settingsmailing.period),
                    start_time=timezone.now(), expires=message.settingsmailing.time_to_end)
            elif message.settingsmailing.time_to_start > current_time:
                PeriodicTask.objects.filter(name=f'mailing list_{message}').update(
                    name=f'mailing list_{message}',
                    interval=IntervalSchedule.objects.get(pk=message.pk, every=message.settingsmailing.every,
                                                          period=message.settingsmailing.period),
                    start_time=message.settings.time_to_start,
                    expires=message.settingsmailing.time_to_end)

        return super().form_valid(form)

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может редактировать рассылки')
        return object_


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_list:home_page')

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может удалять рассылки')
        PeriodicTask.objects.filter(name=f'mailing list_{object_}').delete()
        return object_


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Managers').exists():
            return queryset
        else:
            return queryset.filter(user=self.request.user)


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientAddForm
    success_url = reverse_lazy('mailing_list:home_page')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientUpdateForm
    success_url = reverse_lazy('mailing_list:client_list')

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может редактировать информацию о клиентах')
        return object_


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_list:client_list')

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может удалять клиентов')
        return object_


class LogsListView(ListView):
    model = Logs

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        names_of_messages = Message.objects.all()
        context_data['object_list'] = names_of_messages
        return context_data


class LogsListDetail(DetailView):
    model = Message
    template_name = 'mailing_list/logslist_detail.html'
