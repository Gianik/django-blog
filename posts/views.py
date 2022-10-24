from django.shortcuts import render
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from comments.models import Comments
from likeunlike.models import Likeunlike


class PostDetailView(LoginRequiredMixin, DetailView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):

        context = super(PostDetailView, self).get_context_data()
        post_object = self.object  # this contain the object that the view is operating upon
        context['object'] = post_object

        # Get all comments  related to the Post
        context['comments'] = Comments.objects.filter(post=post_object)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    fields = ['title', 'content']


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/delete.html'

    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False


# Create your views here.
