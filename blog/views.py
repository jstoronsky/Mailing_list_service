from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from blog.forms import BlogAddForm, BlogUpdateForm
from blog.models import Blog


# Create your views here.
class BlogCreateView(CreateView):
    """
    контроллер для создании статьи
    """
    model = Blog
    form_class = BlogAddForm
    success_url = reverse_lazy('blog:blog')

    def form_valid(self, form):
        if form.is_valid:
            object_ = form.save()
            object_.author = self.request.user
            object_.save()
        return super().form_valid(form)
        

class BlogListView(ListView):
    """
    контроллер для спиского отображения статей
    """
    model = Blog


class BlogDetailView(DetailView):
    """
    контроллер для подробного просмотра конкретной статьи
    """
    model = Blog

    def get_object(self, queryset=None):
        """
        метод для изменения количества просмотров
        """
        object_ = super().get_object(queryset)
        object_.views_count += 1
        object_.save()
        return object_


class BlogUpdateView(UpdateView):
    """
    контроллер для изменения информации по статье
    """
    model = Blog
    form_class = BlogUpdateForm
    success_url = reverse_lazy('blog:blog')


class BlogDeleteView(DeleteView):
    """
    контроллер для удаления статьи
    """
    model = Blog
    success_url = reverse_lazy('blog:blog')
