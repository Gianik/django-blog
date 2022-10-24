from django.db import models
from django.utils import timezone
from users.models import User
from posts.models import Post


class Likeunlike(models.Model):
    like = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # def number_of_likes(self):
    #     return self.likes.count()
# Create your models here.
