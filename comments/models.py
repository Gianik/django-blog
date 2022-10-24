from django.db import models
from django.utils import timezone
from users.models import User
from posts.models import Post


class Comments(models.Model):
    text = models.CharField(max_length=100)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
# Create your models here.
