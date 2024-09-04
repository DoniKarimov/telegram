from django.urls import path, include
from .views import *


urlpatterns = [
    path('', Home.as_view(), name = 'home'),
    path('create/', created_name, name = 'create'),
    path('add/members/<int:id>', add_members, name = 'add_members'),
    path('register/', register, name = 'signup'),
    path('profile', profile, name = 'profil'),
    path('channel/', create_channels, name  = 'channels'),
    path('group/', create_group, name = 'group')
]