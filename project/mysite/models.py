from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)

class Post(models.Model):
    title = models.CharField(max_length=50)

