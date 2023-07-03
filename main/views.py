import datetime
import threading
import time

import schedule
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from .forms import MailingForm, ClientForm, MailingAttemptForm
from main.models import Mailing, Client, MailingAttempt
from .tasks import send_mailing_task, start_scheduler


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


class ClientListView(generic.ListView):
    model = Client
    extra_context = {
        'title': 'Все клиенты'
    }

    def get_queryset(self):
        return super().get_queryset().filter(client_owner=self.request.user)

class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/create_client.html'
    success_url = '/client_list/'

    def form_valid(self, form):
        self.object = form.save()
        self.object.client_owner = self.request.user
        form.instance.client_owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_update.html'

    # success_url = 'main/blog_detail/<int:pk>/'  # Перенаправление после успешного создания статьи

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.object.get_absolute_url())


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'main/client_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class ClientDeleteView(generic.DeleteView):
    model = Client    #Модель
    success_url = reverse_lazy('main:client_list')    #Адрес для перенаправления после успешного удаления


class MailingListView(generic.ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'
    extra_context = {
        'title': 'Все рассылки'
    }


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MailingAttemptFormset = inlineformset_factory(Mailing, MailingAttempt, form=MailingAttemptForm, extra=1)
        formset = MailingAttemptFormset
        context['mailing'] = Mailing.objects.all()  # Если только одна рассылка
        context['formset'] = formset  # Добавляем форму в контекст
        return context

    def post(self, request, *args, **kwargs):
        """
        Функция для активации/деактивации шедьюлера
        """
        if 'start_mailing' in request.POST:
            threading.Thread(target=start_scheduler()).start()   # Запуск шедьюлера в отдельном потоке
            print('Рассылки запущены')
        elif 'stop_mailing' in request.POST:
            schedule.clear()
            print('Рассылки остановлены')
        return self.get(request, *args, **kwargs)


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/create_mailing.html'
    success_url = '/mailing_list/'

    def form_valid(self, form):
        # Создание экземпляра Mailing
        self.object = form.save()
        self.object.mailing_owner = self.request.user
        form.instance.mailing_owner = self.request.user
        self.object.save()
        formset = self.get_form()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        # Создание первой MailingAttempt
        send_datetime = timezone.now()
        mailing_attempt = MailingAttempt.objects.create(mailing=self.object, send_datetime=send_datetime, status='failure',server_response='create')
        mailing_attempt.save()
        return super().form_valid(form)


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(client_owner=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_form()
        return context
    #def form_valid(self, form):
    #Отправка на электронку при создании новой рассылки
    #   obj = form.save()
    #    send_mailing_task(obj)
    #    return super().form_valid(form)


class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter'] = Mailing.objects.first()  # Предположим, что вы выбираете только одну рассылку
        return context


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_update.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.object.get_absolute_url())


class MailingDeleteView(generic.DeleteView):
    model = Mailing  # Модель
    success_url = reverse_lazy('main:mailing_list')  # Адрес для перенаправления после успешного удаления
