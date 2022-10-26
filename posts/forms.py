from django import forms
from .models import Post, Comments


class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content")


class CommentCreationForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ("text",)
