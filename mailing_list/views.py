from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from mailing_list.forms import MessageAddForm, MessageUpdateForm, ClientAddForm, ClientUpdateForm, CustomIntervalAddForm
from mailing_list.models import Client, Message, Logs, CustomInterval
from django.forms import inlineformset_factory


# Create your views here.
class MailingHomepage(TemplateView):
    template_name = 'mailing_list/home_page.html'


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageAddForm
    success_url = reverse_lazy('mailing_list:home_page')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        interval_form_set = inlineformset_factory(Message, CustomInterval, form=CustomIntervalAddForm, extra=1)
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
        return super().form_valid(form)

    # def form_valid(self, form):
    #     send_mailing()
    #     return super(MessageCreateView, self).form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageUpdateForm
    success_url = reverse_lazy('mailing_list:message_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        interval_form_set = inlineformset_factory(Message, CustomInterval, form=CustomIntervalAddForm, extra=1)
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
        return super().form_valid(form)


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_list:home_page')


class ClientListView(ListView):
    model = Client


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


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_list:home_page')


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
