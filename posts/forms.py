from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "content")

    def clean_title(self,  *args, **kwargs):
        title = self.cleaned_data.get("title")

        if len(title) > 100:
            raise forms.ValidationError(
                "Blog Title Input exceeds max length")
        return title

    def clean_content(self,  *args, **kwargs):
        content = self.cleaned_data.get("content")

        if len(content) > 255:
            raise forms.ValidationError(
                "Blog Content Input exceeds max length")
        return content


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ("text",)

    def clean_text(self,  *args, **kwargs):
        text = self.cleaned_data.get("text")

        if len(text) > 100:
            raise forms.ValidationError(
                "Comment Text Input exceeds max length")
        return text
