from django.urls import reverse_lazy

from .models import BlogModel
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class BlogListView(ListView):
    model = BlogModel
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogModel
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count = (obj.views_count or 0) + 1
        obj.save(update_fields=['views_count'])
        return obj


class BlogCreateView(CreateView):
    model = BlogModel
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = BlogModel
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/blog_form.html'
    pk_url_kwarg = 'blog_id'

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'blog_id': self.object.id})


class BlogDeleteView(DeleteView):
    model = BlogModel
    template_name = 'blog/blog_confirm_delete.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blog:blog_list')
    pk_url_kwarg = 'blog_id'
