from django.urls import reverse_lazy

from .models import BlogModel
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class BlogListView(ListView):
    model = BlogModel
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    model = BlogModel
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_id'


class BlogCreateView(CreateView):
    model = BlogModel
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = BlogModel
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')
    pk_url_kwarg = 'blog_id'


class BlogDeleteView(DeleteView):
    model = BlogModel
    template_name = 'blog/blog_confirm_delete.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blog:blog_list')
    pk_url_kwarg = 'blog_id'
