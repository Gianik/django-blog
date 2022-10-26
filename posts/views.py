from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView)
from .models import Post, Comments
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostDetailView(LoginRequiredMixin, DetailView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):

        context = super(PostDetailView, self).get_context_data()
        # this contain the object that the view is operating upon
        post_object = self.object
        context['object'] = post_object

        liked = False
        if post_object.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['comments'] = Comments.objects.filter(post=post_object)
        context['likes'] = post_object.number_of_likes()
        context['is_liked'] = liked

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

    def handle_no_permission(self):
        return redirect('blog-detail', self.kwargs['pk'])


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/delete.html'

    def test_func(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data()  # get context

        # find the post object that will be deleted
        post_object = get_object_or_404(Post, id=self.kwargs['pk'])
        context['object'] = post_object

        return context

    def post(self, request,  *args, **kwargs):
        # import pdb
        # pdb.set_trace()

        self_object = get_object_or_404(Post, id=self.kwargs['pk'])
        self_object.delete()

        return redirect('blog-home')

    def handle_no_permission(self):
        return redirect('blog-detail', self.kwargs['pk'])


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
        # form.instance.post = get_object_or_404(Comments, id=self.request.post.id)

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

    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('blog-detail', kwargs={'pk': post.id})

    def test_func(self):
        comments = self.get_object()
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False


class LikeunlikeView(LoginRequiredMixin, TemplateView):
    # import pdb
    # pdb.set_trace()
    model = Post

    def post(self, request,  *args, **kwargs):

        self_object = get_object_or_404(Post, id=self.kwargs['pk'])
        post_object = self_object
        post_id = self.kwargs['pk']
        if post_object.likes.filter(id=request.user.id).exists():
            post_object.likes.remove(request.user)
        else:
            post_object.likes.add(request.user)

        return redirect('blog-detail', post_id)

        # Create your views here.
