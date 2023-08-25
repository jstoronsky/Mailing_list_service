import random
import string

from django.contrib.auth.views import LoginView
from users.models import User
from users.forms import RegisterForm, ChangeForm, LoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, UpdateView, ListView
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from config import settings


# Create your views here.
class RegisterView(CreateView):
    """
    контроллер для регистрации
    """
    model = User
    form_class = RegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('users:activate')

    def form_valid(self, form):
        """
        здесь отправляем на почту код активации
        """
        user = form.save()
        subject = 'Активация аккаунта'
        num1 = str(random.randint(0, 9))
        num2 = str(random.randint(0, 9))
        num3 = str(random.randint(0, 9))
        num4 = str(random.randint(0, 9))
        random_code_list = [num1, num2, num3, num4]
        random_code = ''.join(random_code_list)
        user.verification_key = random_code
        user.save()
        message = f'{user.first_name}, введите данный код: {user.verification_key}, чтобы активировать ваш аккаунт'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        return super().form_valid(form)


def activate_email(request):
    """
    функция-контроллер для проверки правильности кода активации
    """
    if request.method == 'POST':
        get_code = request.POST.get('code')

        try:
            user = User.objects.get(verification_key=get_code)
        except ObjectDoesNotExist:
            return HttpResponse('Вы ввели неверный код!')

        else:
            user.is_active = True
            user.save()
            return HttpResponse('Ваш аккаунт активирован! Теперь вы можете им пользоваться')

    return render(request, 'users/activation_check.html')


def reset_password(request):
    """
    функция-контроллер для сброса пароля
    """
    if request.method == 'POST':
        get_email = request.POST.get('email')
        letters = list(string.ascii_letters)
        new_password = []
        for index in range(0, 9):
            digit = random.choice(letters)
            new_password.append(digit)
        new_password_ = ''.join(new_password)
        try:
            user = User.objects.get(email=get_email)
        except ObjectDoesNotExist:
            return render(request, 'users/unsuccessful_reset.html')
        else:
            user.set_password(new_password_)
            subject = 'Сброс пароля'
            message = f'{user.first_name}, ваш пароль был сброшен. Ваш новый пароль: {new_password_}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            user.save()
            return render(request, 'users/successful_reset.html')
            # return HttpResponse('Новый пароль отправлен на вашу электронную почту!')
    return render(request, 'users/password_reset.html')


class UserLogin(LoginView):
    """
    контроллер для аутентификации
    """
    form_class = LoginForm
    template_name = 'users/login.html'


class ChangeView(UpdateView):
    """
    контроллер для аутентификации
    """
    model = User
    form_class = ChangeForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('mailing_list:home_page')

    def get_object(self, queryset=None):
        return self.request.user


class UsersList(ListView):
    """
    контроллер отображения списка зарегистрированных пользователей, нужно для реализации бана
    """
    model = User
    template_name = 'users/users_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset.exclude(is_superuser=True)
        return queryset.exclude(is_staff=True)


class UserDeactivate(UpdateView):
    """
    контроллер для бана, доступно менеджерам и суперюзеру
    """
    model = User
    fields = ('is_active',)
    template_name = 'users/user_deactivation.html'
    success_url = reverse_lazy('users:users_list')
