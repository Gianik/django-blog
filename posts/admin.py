from django.contrib import admin

from posts.models import Post, Likeunlike, Comments

admin.site.register(Post)
admin.site.register(Likeunlike)
admin.site.register(Comments)


# Register your models here.
