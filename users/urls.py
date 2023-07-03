from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, VerifyEmailView, VerifyEmailSentView, EmailConfirmedView, \
    UserPasswordResetView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, UserPasswordResetDoneView

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('verify_email_sent/', VerifyEmailSentView.as_view(), name='verify_email_sent'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<str:uidb64>/<str:token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]