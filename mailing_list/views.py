from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from django_celery_beat.models import PeriodicTask
from config.settings import CACHE_ENABLED
from django.core.cache import cache
from mailing_list.forms import MessageAddForm, MessageUpdateForm, ClientAddForm, ClientUpdateForm, SettingsAddForm, \
    SettingsChangeStatus
from mailing_list.models import Client, Message, Logs, SettingsMailing
from blog.models import Blog
from django.forms import inlineformset_factory


# Create your views here.
class MailingHomepage(TemplateView):
    """
    контроллер главной страницы
    """
    template_name = 'mailing_list/home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        здесь,во-первых, добавление в контексный менеджер моделей клиента и сообщений для вывода подсчёта
        а, во-вторых, вывод трёх статей из блога и их кеширование
        """
        context_data = super().get_context_data(**kwargs)
        all_messages = len(Message.objects.all())
        active_messages = len(SettingsMailing.objects.filter(status='Активна'))
        all_clients = len(Client.objects.all())
        context_data['all_messages'] = all_messages
        context_data['active_messages'] = active_messages
        context_data['all_clients'] = all_clients
        if CACHE_ENABLED:
            key = f'blog_list'
            blogs = cache.get(key)
            context_data['blogs'] = blogs
            if blogs is None:
                blog_list = Blog.objects.all()[:3]
                cache.set(key, blog_list)
        else:
            blogs = Blog.objects.all()[:3]
            context_data['blogs'] = blogs
        return context_data


class MessageListView(ListView):
    """
    Вывод списка рассылок
    """
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Managers').exists():
            return queryset
        else:
            return queryset.filter(user=self.request.user)


class MessageDetailView(DetailView):
    """
    Контроллер для конкретной рассылки
    """
    model = Message

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients = SettingsMailing.objects.get(message=self.object).clients.all()
        clients_ = [client.email for client in clients]
        context_data['clients'] = ", ".join(clients_)
        return context_data


class MessageCreateView(CreateView):
    """
    Контроллер для создания рассылки
    """
    model = Message
    form_class = MessageAddForm
    success_url = reverse_lazy('mailing_list:message_list')

    def get_context_data(self, **kwargs):
        """
        здесь мы пользуемся inlineformset_factory, чтобы подмешать к созданию сообщения рассылки её настройки
        """
        context_data = super().get_context_data(**kwargs)
        interval_form_set = inlineformset_factory(Message, SettingsMailing, form=SettingsAddForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = interval_form_set(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = interval_form_set(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        здесь при условии валидности формы создаём экземпляр модели PeriodicTask, которая у нас отвечает за работу
        переодических задач в celery. После создания экземпляра открываем файл tasks.py и записываем туда функцию
        для переодической задачи. Функция у нас привязывается к только что созданному экземляру PeriodicTask
        """
        formset = self.get_context_data()['formset']
        object_ = form.save()
        if formset.is_valid():
            formset.instance = object_
            formset.save()
            message = object_
            current_time = timezone.now()
            if message.settingsmailing.time_to_start <= current_time:
                PeriodicTask.objects.create(name=f'mailing list_{message}', task=f'send_mail_{object_.pk}_to_clients',
                                            interval=SettingsMailing.objects.get(message=message),
                                            start_time=timezone.now(), expires=message.settingsmailing.time_to_end,
                                            enabled=False)
            elif message.settingsmailing.time_to_start > current_time:
                PeriodicTask.objects.create(name=f'mailing list_{message}', task=f'send_mail_{object_.pk}_to_clients',
                                            interval=SettingsMailing.objects.get(message=message),
                                            start_time=message.settingsmailing.time_to_start,
                                            expires=message.settingsmailing.time_to_end,
                                            enabled=False)
            with open('mailing_list/tasks.py', 'at') as tasks:
                function_code = f"""
                
@shared_task(name='send_mail_{message.pk}_to_clients')
def send_mail_to_{message.pk}_clients():
    message = Message.objects.get(pk={message.pk})
    clients = SettingsMailing.objects.get(message=message).clients.all()
    clients_mails = [client.email for client in clients]
    try:
        send_mail(message.header, message.body, settings.EMAIL_HOST_USER, clients_mails)
        message.settingsmailing.status = 'Активна'
        message.settingsmailing.save(update_fields=['status'])
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Отправлено')
        if message.settingsmailing.time_to_end <= timezone.now():
            task = PeriodicTask.objects.get(task=f'send_mail_{message}_to_clients')
            task.enabled = False
            task.save()
            message.settingsmailing.status = 'Не активна'
            message.settingsmailing.save(update_fields=['status'])
    except SMTPException:
        Logs.objects.create(message=message, datetime_of_attempt=timezone.now(), status='Не отправлено')
        task = PeriodicTask.objects.get(task=f'send_mail_{message}')
        task.enabled = False
        task.save()
        message.settingsmailing.status = 'Не активна'
        message.settingsmailing.save(update_fields=['status'])

"""
                tasks.write(function_code)
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    """
    контроллер для редактирования рассылки
    функционал почти такой же как в контроллере создания, обновление рассылки приводит и к обновлению переодической
    задачи, связанной с этой рассылкой
    """
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
                if message.settingsmailing.status == 'Не активна':
                    PeriodicTask.objects.filter(name=f'mailing list_{message}').update(enabled=False)
                elif message.settingsmailing.status == 'Активна':
                    PeriodicTask.objects.filter(name=f'mailing list_{message}').update(enabled=True)
                PeriodicTask.objects.filter(name=f'mailing list_{message}').update(
                    name=f'mailing list_{message}', interval=SettingsMailing.objects.get(message=message),
                    start_time=timezone.now(), expires=message.settingsmailing.time_to_end)
            elif message.settingsmailing.time_to_start > current_time:
                if message.settingsmailing.status == 'Не активна':
                    PeriodicTask.objects.filter(name=f'mailing list_{message}').update(enabled=False)
                elif message.settingsmailing.status == 'Активна':
                    PeriodicTask.objects.filter(name=f'mailing list_{message}').update(enabled=True)
                PeriodicTask.objects.filter(name=f'mailing list_{message}').update(
                    name=f'mailing list_{message}',
                    interval=SettingsMailing.objects.get(message=message),
                    start_time=message.settingsmailing.time_to_start,
                    expires=message.settingsmailing.time_to_end)

        return super().form_valid(form)

    # def get_object(self, queryset=None):
    #     object_ = super().get_object(queryset)
    #     if self.request.user.groups.filter(name='Managers').exists():
    #         raise Http404('Пользователь из вашей группы доступа не может редактировать рассылки')
    #     return object_


class MessageDeleteView(DeleteView):
    """
    контроллер для удаления рассылки, удаляется также и переодическая задача
    """
    model = Message
    success_url = reverse_lazy('mailing_list:message_list')

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может удалять рассылки')
        PeriodicTask.objects.filter(name=f'mailing list_{object_}').delete()
        return object_


class ClientListView(ListView):
    """
    контроллер для вывода списка клиентов
    """
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Managers').exists():
            return queryset
        else:
            return queryset.filter(user=self.request.user)


class ClientDetailView(DetailView):
    """
    контроллер для детального просмотра информации о клиенте
    """
    model = Client


class ClientCreateView(CreateView):
    """
    контроллер для добавления клиента
    """
    model = Client
    form_class = ClientAddForm
    success_url = reverse_lazy('mailing_list:home_page')


class ClientUpdateView(UpdateView):
    """
    контроллер для обновления информации о клиенте
    """
    model = Client
    form_class = ClientUpdateForm
    success_url = reverse_lazy('mailing_list:client_list')

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может редактировать информацию о клиентах')
        return object_


class ClientDeleteView(DeleteView):
    """
    контроллер для удаления клиента
    """
    model = Client
    success_url = reverse_lazy('mailing_list:client_list')

    def get_object(self, queryset=None):
        object_ = super().get_object(queryset)
        if self.request.user.groups.filter(name='Managers').exists():
            raise Http404('Пользователь из вашей группы доступа не может удалять клиентов')
        return object_


class LogsListView(ListView):
    """
    контроллер вывода списка рассылок, по которым можно просмотреть логи
    """
    model = Logs

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        names_of_messages = Message.objects.all()
        context_data['object_list'] = names_of_messages
        return context_data


class LogsListDetail(DetailView):
    """
    контроллер для вывода логов конкретной рассылки
    """
    model = Message
    template_name = 'mailing_list/logslist_detail.html'


class ChangeStatus(UpdateView):
    """
    контроллер для изменения статуса рассылки. Для менеджеров
    """
    model = SettingsMailing
    form_class = SettingsChangeStatus
    template_name = 'mailing_list/change_status.html'
    success_url = reverse_lazy('mailing_list:message_list')
