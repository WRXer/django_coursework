from django.views import generic

from blog.forms import BlogForm
from blog.models import BlogPost
from django.http import JsonResponse
from blog.models import BlogPost


# Create your views here.
class BlogListView(generic.ListView):
    model = BlogPost

    def get_queryset(self):
        """
        Фильтруйте статьи по положительному признаку публикации
        """
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(generic.DetailView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blog/blog_detail.html'



    def get(self, request, *args, **kwargs):
        """
        Увеличиваем счетчик просмотров
        """
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


def increase_views(request, post_id):
    try:
        blog_post = BlogPost.objects.get(pk=post_id)
        blog_post.views += 1
        blog_post.save()
        return JsonResponse({'status': 'success', 'views': blog_post.views})
    except BlogPost.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Blog post not found'}, status=404)
