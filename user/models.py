from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from animation.models import Genre

# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = "user"
    fav_genre = models.ManyToManyField(Genre, related_name='users')
