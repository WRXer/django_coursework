from django.shortcuts import render
from django.views import generic

from blog.models import BlogPost


# Create your views here.
class BlogsListView(generic.ListView):
    model = BlogPost
    extra_context = {
        'title': 'Блог'
    }


    def get_queryset(self):
        """
        Фильтруйте статьи по положительному признаку публикации
        """
        return BlogPost.objects.filter(is_published=True)


class BlogsDetailView(generic.DetailView):
    model = BlogPost

    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        """
        Увеличиваем счетчик просмотров
        """
        self.object = self.get_object()
        self.object.blog_views += 1
        self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)