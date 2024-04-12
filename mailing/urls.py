from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import HomePageView, MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, LogListView, active_toggle, MessageListView, \
    MessageCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(HomePageView.as_view()), name='home'),

    path('list/', MailingListView.as_view(), name='mailing_list'),
    path('view/<int:pk>/', MailingDetailView.as_view(), name='mailing_view'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_confirm_delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),

    path('log_list/', LogListView.as_view(), name='log_list'),
    path('activity/<int:pk>/', active_toggle, name='activity')
]