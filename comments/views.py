from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
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


class UpdateCommentView(LoginRequiredMixin, UpdateView):

    model = Comments
    fields = ['text']
    template_name = 'comments/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        #form.instance.post = get_object_or_404(Comments, id=self.request.post.id)

        return super().form_valid(form)

    def test_func(self):
        comments = self.get_object()
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Comments
    template_name = 'comments/comment_delete.html'
    success_url = '/'

    def test_func(self):
        comments = self.get_object()
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False


# Create your views here.
