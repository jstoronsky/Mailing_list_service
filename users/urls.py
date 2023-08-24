from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ChangeView, UserLogin, \
    activate_email, reset_password, UsersList, UserDeactivate

app_name = UsersConfig.name

urlpatterns = [path('register/', RegisterView.as_view(), name='register'),
               path('login/', UserLogin.as_view(), name='login'),
               path('logout/', LogoutView.as_view(), name='logout'),
               path('profile/', ChangeView.as_view(), name='profile'),
               path('activate/', activate_email, name='activate'),
               path('reset/', reset_password, name='reset'),
               path('success_reset/', reset_password, name='successful_reset'),
               path('error_reset/', reset_password, name='error_reset'),
               path('user_deactivate/<int:pk>', UserDeactivate.as_view(), name='user_deactivate'),
               path('users_list/', UsersList.as_view(), name='users_list')]
