from django.urls import path

from blog.views import BlogDetailView
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),


]