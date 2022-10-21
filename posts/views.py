from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# class PostListView(ListView):
#     model = Post


class PostDetailView(DetailView):
    #     # import pdb
    #     # pdb.set_trace()
    model = Post
    template_name = 'posts/detail.html'

# Create your views here.
