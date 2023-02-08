from django.db import models

class Picture(models.Model):
    url = models.URLField()