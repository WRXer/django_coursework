from django.urls import path, include
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import index, MailingCreateView, MailingListView, MailingDetailView, ClientListView, ClientDetailView, \
    ClientCreateView, ClientUpdateView, MailingUpdateView, ClientDeleteView, MailingDeleteView
from main.tasks import send_mailing_task


app_name = MainConfig.name
urlpatterns = [
    path('', cache_page(60)(index), name='index'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('send_mailing/', send_mailing_task, name='send_emails'),

]
