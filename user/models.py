from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from animation.models import Genre
# from detail.models import Recommend


class UserModel(AbstractUser):
    class Meta:
        db_table = "user"
    fav_genre = models.ManyToManyField(Genre, related_name='users')
    userid = models.CharField(max_length=70, default='')

