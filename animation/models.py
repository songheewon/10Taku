from django.db import models


# Create your models here.

class Genre(models.Model):
    class Meta:
        db_table = "genre"
    name = models.CharField(max_length=70, default='')

class Animation(models.Model):
    class Meta:
        db_table = "animation"
    name = models.CharField(max_length=70, default='')
    thumbnail = models.TextField(max_length=256, default='')
    publisher = models.CharField(max_length=70, default='')
    summary = models.TextField(max_length=256, default='')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

