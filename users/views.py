from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth import login
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
import config.settings


# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    # success_url = reverse_lazy('users:verify_email_sent')

    def form_valid(self, form):
        new_user = form.save()
        token = default_token_generator.make_token(new_user)
        uid = new_user.pk
        verification_link = reverse_lazy('users:verify_email', kwargs={'uidb64': uid, 'token': token})
        site = config.settings.SITE_ADRES
        send_mail(
            subject='Поздравляем Вас с регистрацией!',
            message=f'Вы почти зарегистрировались на нашей платформе! Для активации аккаунта перейдите по ссылке! http://{site}{verification_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        # return super().form_valid(form)
        return redirect('users:verify_email_sent')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = uidb64
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user


class VerifyEmailSentView(View):
    def get(self, request):
        return render(request, 'users/verify_email_sent.html')


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'
    # def get(self, request):
    #    return render(request, 'users/email_confirmed.html')


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'users/registration/password_reset_email.html'
    template_name = 'users/registration/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/registration/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/registration/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/registration/password_reset_complete.html'