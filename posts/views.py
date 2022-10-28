from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Post, Comments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import PostForm, CommentForm


class PostDetailView(TemplateView):

    model = Post
    template_name = 'posts/detail.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            messages.warning(request, 'You are not Authorized')
            return redirect('blog-login')

        if not Post.objects.filter(id=self.kwargs['pk']):
            messages.warning(request, 'Blog Post Not found')
            return redirect('blog-home')

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):

        post_object = get_object_or_404(Post, id=self.kwargs['pk'])

        liked = False
        if post_object.likes.filter(id=self.request.user.id).exists():
            liked = True

        context = {
            "object": post_object,
            "comments": Comments.objects.filter(post=post_object),
            "likes": post_object.number_of_likes(),
            "is_liked": liked
        }

        return context


class PostCreateView(LoginRequiredMixin, TemplateView):
    model = Post
    form = PostForm
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
            messages.success(
                request, 'New Blog post created by {}'.format(request.user))
            return redirect('blog-home')
        else:
            return render(request, self.template_name, {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    model = Post
    form = PostForm
    template_name = 'posts/post_form.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        form = self.form(instance=get_object_or_404(
            Post, id=self.kwargs['pk']))

        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):

        post_object = get_object_or_404(Post, id=self.kwargs['pk'])

        form = self.form(request.POST, instance=post_object)
        form.instance.author = post_object.author
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog Post Updated')
            return redirect('blog-detail', self.kwargs['pk'])
        else:
            return render(request, self.template_name, {'form': form})

    def test_func(self):

        if not Post.objects.filter(id=self.kwargs['pk']):
            messages.warning(self.request, 'Blog Post Not found')
            return redirect('blog-home')

        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect('blog-detail', self.kwargs['pk'])


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    model = Post
    template_name = 'posts/delete.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request,  *args, **kwargs):

        self_object = get_object_or_404(Post, id=self.kwargs['pk'])
        self_object.delete()
        messages.success(request, 'Blog Post Deleted')
        return redirect('blog-home')

    def get_context_data(self, **kwargs):

        context = {"object": get_object_or_404(Post, id=self.kwargs['pk'])}

        return context

    def test_func(self):

        if not Post.objects.filter(id=self.kwargs['pk']):
            messages.warning(self.request, 'Blog Post Not found')
            return redirect('blog-home')

        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect('blog-detail', self.kwargs['pk'])


class CreateCommentView(LoginRequiredMixin, TemplateView):

    model = Comments
    form = CommentForm
    template_name = 'posts/post_form_comment.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        if not Post.objects.filter(id=self.kwargs['post_id']):
            messages.warning(self.request, 'Blog Post Not found')
            return redirect('blog-home')

        form = self.form
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):

        form = self.form(request.POST)
        form.instance.author = request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        if form.is_valid():

            form.save()
            messages.success(request, 'Comment Created')
            return redirect('blog-detail', self.kwargs['post_id'])
        else:
            return render(request, self.template_name, {'form': form})


class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    model = Comments
    form = CommentForm
    template_name = 'posts/post_form_comment.html'

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        form = self.form(instance=get_object_or_404(
            Comments, id=self.kwargs['pk']))
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):

        comment_object = get_object_or_404(Comments, id=self.kwargs['pk'])
        form = self.form(request.POST, instance=comment_object)
        form.instance.author = comment_object.author
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment Updated')
            return redirect('blog-detail', comment_object.post.id)
        else:
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):
        if not Comments.objects.filter(id=self.kwargs['pk']):
            messages.warning(self.request, 'Comment Not found')
            return redirect('blog-home')

        comments = self.get_object()
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        comment_object = comment_object = get_object_or_404(
            Comments, id=self.kwargs['pk'])
        return redirect('blog-detail',  comment_object.post.id)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    model = Comments
    template_name = 'posts/comment_delete.html'

    def get_context_data(self, **kwargs):

        context = {"object": get_object_or_404(Comments, id=self.kwargs['pk'])}

        return context

    def post(self, request,  *args, **kwargs):

        comment_object = get_object_or_404(Comments, id=self.kwargs['pk'])
        comment_object.delete()
        messages.success(request, 'Comment Deleted')
        return redirect('blog-detail', comment_object.post.id)

    def test_func(self):

        if not Comments.objects.filter(id=self.kwargs['pk']):
            messages.warning(self.request, 'Comment Not found')
            return redirect('blog-home')

        comments = get_object_or_404(Comments, id=self.kwargs['pk'])
        if self.request.user == comments.author or self.request.user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        comment_object = comment_object = get_object_or_404(
            Comments, id=self.kwargs['pk'])
        return redirect('blog-detail',  comment_object.post.id)


class LikeunlikeView(LoginRequiredMixin, TemplateView):

    model = Post

    def post(self, request,  *args, **kwargs):

        self_object = get_object_or_404(Post, id=self.kwargs['pk'])
        post_object = self_object
        post_id = self.kwargs['pk']
        if post_object.likes.filter(id=request.user.id).exists():
            post_object.likes.remove(request.user)
        else:
            post_object.likes.add(request.user)
        messages.success(request, 'User has liked Blog Post')
        return redirect('blog-detail', post_id)
