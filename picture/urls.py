from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'picture'

router = DefaultRouter()
router.register('pictures', views.PictureViewSet, basename='picture')

urlpatterns = [
    path('', include(router.urls)),
]