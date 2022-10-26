from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView)
from .models import Post, Comments
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostCreationForm, CommentCreationForm


class PostDetailView(LoginRequiredMixin, TemplateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):

        context = super(PostDetailView, self).get_context_data()
        # this contain the object that the view is operating upon
        post_object = get_object_or_404(Post, id=self.kwargs['pk'])
        context['object'] = post_object

        liked = False
        if post_object.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['comments'] = Comments.objects.filter(post=post_object)
        context['likes'] = post_object.number_of_likes()
        context['is_liked'] = liked

        return context


# class PostCreateView(LoginRequiredMixin, CreateView):
#     #     # import pdb
#     #     # pdb.set_trace()
#     model = Post
#     fields = ['title', 'content']

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, TemplateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    form = PostCreationForm
    template_name = 'posts/post_form.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        form = self.form
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):

        form = self.form(request.POST)
        form.instance.author = request.user
        if form.is_valid():

            form.save()
            return redirect('blog-home')
        else:
            return render(request, self.template_name, {'form': form})


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

       # get the post object to display the post title in the template
        post_object = get_object_or_404(Post, id=self.kwargs['pk'])
        context['object'] = post_object

        return context

    def post(self, request,  *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        # find the post object that will be deleted
        self_object = get_object_or_404(Post, id=self.kwargs['pk'])
        self_object.delete()

        return redirect('blog-home')

    def handle_no_permission(self):
        return redirect('blog-detail', self.kwargs['pk'])


class CreateCommentView(LoginRequiredMixin, TemplateView):

    #     # import pdb
    #     # pdb.set_trace()
    model = Comments
    form = CommentCreationForm
    template_name = 'posts/post_form_comment.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        form = self.form
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):

        form = self.form(request.POST)
        form.instance.author = request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if form.is_valid():

            form.save()
            return redirect('blog-detail', self.kwargs['post_id'])
        else:
            return render(request, self.template_name, {'form': form})


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


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Comments
    template_name = 'posts/comment_delete.html'

    def test_func(self):
        comments = get_object_or_404(Comments, id=self.kwargs['pk'])
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView,
                        self).get_context_data()  # get context

       # get the post object to display the post title in the template
        comment_object = get_object_or_404(Comments, id=self.kwargs['pk'])
        context['object'] = comment_object

        return context

    def post(self, request,  *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        # find the comment object that will be deleted
        comment_object = get_object_or_404(Comments, id=self.kwargs['pk'])
        comment_object.delete()

        return redirect('blog-detail', comment_object.post.id)

    def handle_no_permission(self):
        comment_object = comment_object = get_object_or_404(
            Comments, id=self.kwargs['pk'])
        return redirect('blog-detail',  comment_object.post.id)


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
