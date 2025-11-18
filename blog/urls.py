from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/list/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:blog_id>/',BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create/',  BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:blog_id>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:blog_id>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
]
