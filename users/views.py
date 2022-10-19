from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm
from posts.models import Post


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'users/home.html', context)


def about(request):
    return render(request, 'users/about.html')


def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# Create your views here.
