from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import MailingForm
from main.models import Mailing


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/create_mailing.html'


class MailingDetailView(generic.DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/update_mailing.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.object.get_absolute_url())


class MailingDeleteView(generic.DeleteView):
    model = Mailing  # Модель
    success_url = reverse_lazy('main/mailing_list.html')  # Адрес для перенаправления после успешного удаления
