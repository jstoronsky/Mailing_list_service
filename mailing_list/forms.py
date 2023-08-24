from django import forms
from mailing_list.models import Client, Message, SettingsMailing


class MixinStyle:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('header', 'body', 'user')
        # fields = '__all__'
        # exclude = ('product_image')


class MessageUpdateForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('header', 'body')
        # fields = '__all__'
        # exclude = ('product_image')


class ClientAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('last_name', 'first_name', 'middle_name', 'email', 'commentary', 'user')


class ClientUpdateForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class SettingsAddForm(MixinStyle, forms.ModelForm):
    class Meta:
        model = SettingsMailing
        fields = '__all__'
