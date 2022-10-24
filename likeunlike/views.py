from django.shortcuts import render
from posts.models import Post
from .models import Likeunlike
from django.views.generic import TemplateView
from django.views.generic import DetailView


class LikeUnlikeView(DetailView):

    model = Likeunlike

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)


# Create your views here.
