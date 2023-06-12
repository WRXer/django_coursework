from django.urls import path
from main.apps import MainConfig
from main.views import index, MailingCreateView, MailingListView

app_name = MainConfig.name
urlpatterns = [
    path('', index, name='index'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
]
