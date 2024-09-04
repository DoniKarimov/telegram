from django.urls import path, include
from chat.views import *

urlpatterns = [
    path('', Home.as_view(), name = 'home'),

]