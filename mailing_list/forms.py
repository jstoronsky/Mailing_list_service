from django import forms
from mailing_list.models import Client, Message, SettingsMailing


class MixinStyle:
    """
    стиль для форм
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MessageAddForm(MixinStyle, forms.ModelForm):
    """
    форма для создания сообщения рассылки
    """
    class Meta:
        model = Message
        fields = ('header', 'body', 'user')
        # fields = '__all__'
        # exclude = ('product_image')


class MessageUpdateForm(MixinStyle, forms.ModelForm):
    """
    форма для изменения сообщения рассылки
    """
    class Meta:
        model = Message
        fields = ('header', 'body')
        # fields = '__all__'
        # exclude = ('product_image')


class ClientAddForm(MixinStyle, forms.ModelForm):
    """
    форма для добавления клиента
    """
    class Meta:
        model = Client
        fields = ('last_name', 'first_name', 'middle_name', 'email', 'commentary', 'user')


class ClientUpdateForm(MixinStyle, forms.ModelForm):
    """
    форма для обновления информации о клиенте
    """
    class Meta:
        model = Client
        fields = '__all__'


class SettingsAddForm(MixinStyle, forms.ModelForm):
    """
    форма для создания настроек рассылки, подмешивается к форме сообщения
    """
    class Meta:
        model = SettingsMailing
        fields = '__all__'


class SettingsChangeStatus(MixinStyle, forms.ModelForm):
    """
    форма для изменения статуса рассылки, нужна для группы пользователей 'менеджер'
    """
    class Meta:
        model = SettingsMailing
        fields = ('message', 'status', )
