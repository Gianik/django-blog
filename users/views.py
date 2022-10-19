from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserCreationForm
from posts.models import Post
from django.contrib import messages


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'users/home.html', context)


def about(request):
    return render(request, 'users/about.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account Created for {email}!')

            return redirect('blog-home')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# Create your views here.
