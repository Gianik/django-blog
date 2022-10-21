from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView)
from .models import Post


# class PostListView(ListView):
#     model = Post


class PostDetailView(DetailView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/detail.html'


class PostCreateView(CreateView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

# Create your views here.
