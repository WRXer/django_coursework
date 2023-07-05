from blog.models import BlogPost
from django import forms


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
