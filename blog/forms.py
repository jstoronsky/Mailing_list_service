from django import forms
from blog.models import Blog


class MixinStyle:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('header', 'content', 'preview', 'date_when_created', 'author')


class BlogUpdateForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('header', 'content', 'preview', 'date_when_created', 'author')
