from django.db import models


# Create your models here.

class Genre(models.Model):
    class Meta:
        db_table = "genre"
    name = models.CharField(max_length=70, default='')

class Animation(models.Model):
    class Meta:
        db_table = "animation"
    title = models.CharField(max_length=70, default='')
    original_title = models.CharField(max_length=70, default='')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    publisher = models.CharField(max_length=70, default='')
    rated = models.CharField(max_length=70, default='')
    broadcasted_date = models.CharField(max_length=70, default='')
    chapters = models.CharField(max_length=70, default='')
    summary = models.TextField(max_length=256, default='')
    img = models.TextField(max_length=256, default='')




