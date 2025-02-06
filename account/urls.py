from django.urls import path
from .views import (UserCreateView, UserLoginView, UserPofileView,
                    UserChangePasswordView, UserResetPasswordView,
                    UserResetPasswordConfirmView)


app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('profile/', UserPofileView.as_view(), name='user_profile'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('reset_password/', UserResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_confirm/', UserResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]