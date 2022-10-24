from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comments


class CreateCommentView(LoginRequiredMixin, CreateView):

    model = Comments
    template_name = 'comments/post_form.html'
    fields = ['text']

    # Create your views here.
