from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post, Comments, Likeunlike
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        context['likes'] = Likeunlike.objects.filter(post=post_object)
        context['is_liked'] = Likeunlike.objects.filter(post=post_object).filter(
            id=self.request.user.id).exists()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.get_object().author

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


class CreateCommentView(LoginRequiredMixin, CreateView):

    model = Comments
    template_name = 'posts/post_form_comment.html'
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])

        return super().form_valid(form)


class UpdateCommentView(LoginRequiredMixin, UpdateView):

    model = Comments
    fields = ['text']
    template_name = 'posts/post_form_comment.html'

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
    template_name = 'posts/comment_delete.html'
    success_url = '/'

    def test_func(self):
        comments = self.get_object()
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False


# Create your views here.
