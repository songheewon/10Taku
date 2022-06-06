from django.db import models
from animation.models import Animation
from user.models import UserModel
# Create your models here.
class Comment(models.Model):
    class Meta:
        db_table = "comment"
    animation = models.ForeignKey(Animation, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bookmark(models.Model):
    class Meta:
        db_table = "bookmark"
    animation = models.ForeignKey(Animation, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

class Recommend(models.Model):
    class Meta:
        db_table = "recommend"
    animation = models.ForeignKey(Animation, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)