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
    extra_context = {
        'title': 'Все рассылки'
    }


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/create_mailing.html'
    success_url = '/mailing_list/'

    #def form_valid(self, form):
    #   obj = form.save()
    #    send_mailing_task(obj)
    #    return super().form_valid(form)


class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


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


def status_sending(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    mailing.status_sending()  # Изменить статус на "Запущена"
    return redirect('main:mailing_list')