from django import forms
from mailing_list.models import Client, Message, CustomInterval


class MixinStyle:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('header', 'body', 'time_to_start', 'time_to_end')
        # fields = '__all__'
        # exclude = ('product_image')


class MessageUpdateForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('header', 'body', 'time_to_start', 'time_to_end')
        # fields = '__all__'
        # exclude = ('product_image')


class ClientAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('last_name', 'first_name', 'middle_name', 'email', 'commentary')


class ClientUpdateForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class CustomIntervalAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = CustomInterval
        fields = '__all__'
