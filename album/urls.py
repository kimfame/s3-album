from django.urls import path
from . import views

app_name = 'album'

urlpatterns = [
    path('', views.index),
    path('index', views.index),
]