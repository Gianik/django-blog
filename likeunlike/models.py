from django.db import models
from django.utils import timezone
from users.models import User
from posts.models import Post


class Likeunlike(models.Model):
    like = models.BooleanField(default=False)
    #unlike = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
# Create your models here.
