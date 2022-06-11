from django.db import models
from django.contrib.auth.models import AbstractUser
from animation.models import Genre



class UserModel(AbstractUser):
    class Meta:
        db_table = "user"
    fav_genre = models.ManyToManyField(Genre, related_name='users')
    userid = models.CharField(max_length=70, default='')


