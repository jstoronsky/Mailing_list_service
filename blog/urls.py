from django.urls import path

from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogDeleteView, BlogUpdateView
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
                path('create/', BlogCreateView.as_view(), name='create'),
                path('blog/', BlogListView.as_view(), name='blog'),
                path('article/<int:pk>/', BlogDetailView.as_view(), name='article'),
                path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
                path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete')
]
