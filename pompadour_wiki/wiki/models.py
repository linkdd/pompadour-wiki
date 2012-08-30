from django.db import models

class Wiki(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    gitdir = models.CharField(max_length=512)

# Create your models here.
