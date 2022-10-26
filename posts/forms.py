from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ("text",)
