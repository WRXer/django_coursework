import datetime
import time

import schedule
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import MailingForm, ClientForm
from main.models import Mailing, Client
from .tasks import send_mailing_task


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


class ClientListView(generic.ListView):
    model = Client
    extra_context = {
        'title': 'Все клиенты'
    }


class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/create_client.html'
    success_url = '/client_list/'


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
    last_sent_time = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter'] = Mailing.objects.all()  # Если только одна рассылка
        return context

    def post(self, request, *args, **kwargs):
        mailing_list = Mailing.objects.all()  #Если только одна рассылка
        for mailing in mailing_list:
            if 'start_mailing' in request.POST:
                if mailing.status != 'running':
                    mailing.status = 'running'
                    mailing.save()
                    # Проверка выбранного периода рассылки
                    if mailing.frequency == 'daily':    # Планирование рассылки раз в день
                        self.schedule_mailing(mailing)
                        schedule.every().seconds.do(lambda: self.schedule_mailing(mailing))
                    elif mailing.frequency == 'weekly':     # Планирование рассылки раз в неделю (в указанный день и время)
                        self.schedule_mailing(mailing)
                        schedule.every().seconds.do(lambda: self.schedule_mailing(mailing))
                    elif mailing.frequency == 'monthly':    # Планирование рассылки раз в месяц (в указанный день и время)
                        self.schedule_mailing(mailing)
                        schedule.every().day.at(mailing.start_time).do(lambda: self.schedule_mailing(mailing))

                    #schedule.every().seconds.do(lambda: self.schedule_mailing(mailing))
                    while True:    # Запуск цикла для непрерывного выполнения задач
                        schedule.run_pending()
                        time.sleep(5)
                elif mailing.status == 'running':
                    mailing.status = 'completed'
                    mailing.save()
                    schedule.clear()
                    print("Рассылка остановлена")
            return self.get(request, *args, **kwargs)

    def schedule_mailing(self, mailing):
        """
        Шедьюл отправка рассылки
        """
        current_time = datetime.datetime.now()
        if self.last_sent_time is None or (current_time - self.last_sent_time).total_seconds() >= 10:  # Проверяем, прошло ли подходящее время
            send_mailing_task()
            self.last_sent_time = current_time
            print("Рассылка отправлена")


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/create_mailing.html'
    success_url = '/mailing_list/'

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
