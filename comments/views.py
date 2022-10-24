from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comments
from posts.models import Post


class CreateCommentView(LoginRequiredMixin, CreateView):

    model = Comments
    template_name = 'comments/post_form.html'
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user

        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])

        return super().form_valid(form)

    # Create your views here.
