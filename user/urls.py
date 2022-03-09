from django.urls import path
from user.views import (
    registration, 
    GetUsers, 
    login, 
    refreshed_token,
    )

app_name = 'user'

urlpatterns = [
    path('register', registration, name='user-registration-api'),
    path('login', login, name='user-login-api'),
    path('list', GetUsers.as_view(), name='user-list-api'),
    path('refresh_token', refreshed_token, name='user-token-refresh-api'),
]