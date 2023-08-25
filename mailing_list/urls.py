from django.urls import path
from mailing_list.views import MailingHomepage, ClientCreateView, MessageCreateView, MessageListView, ClientListView, \
    MessageDeleteView, ClientDeleteView, MessageDetailView, ClientDetailView, ClientUpdateView, LogsListView, \
    MessageUpdateView, LogsListDetail, ChangeStatus
from mailing_list.apps import MailingListConfig

app_name = MailingListConfig.name

urlpatterns = [path('', MailingHomepage.as_view(), name='home_page'),
               path('message_list/', MessageListView.as_view(), name='message_list'),
               path('client_list/', ClientListView.as_view(), name='client_list'),
               path('add_client/', ClientCreateView.as_view(), name='add_client'),
               path('add_message/', MessageCreateView.as_view(), name='add_message'),
               path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
               path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
               path('message/<int:pk>', MessageDetailView.as_view(), name='message'),
               path('client/<int:pk>', ClientDetailView.as_view(), name='client'),
               path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
               path('logs/', LogsListView.as_view(), name='logs'),
               path('logsdetail/<int:pk>', LogsListDetail.as_view(), name='logsdetail'),
               path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
               path('change_status/<int:pk>', ChangeStatus.as_view(), name='change_status')
               ]
