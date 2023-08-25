from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from users.models import User


class RegisterForm(UserCreationForm):
    """
    форма для регистрации
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'country', 'avatar')


class ChangeForm(UserChangeForm):
    """
    форма для редактирования данных пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'country', 'avatar', 'is_active')


class LoginForm(AuthenticationForm):
    pass
