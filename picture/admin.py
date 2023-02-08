from django.contrib import admin
from .models import Picture

@admin.register(Picture)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'url',)
