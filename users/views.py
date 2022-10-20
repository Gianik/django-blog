from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserCreationForm, UserUpdateForm
from posts.models import Post
from django.contrib import messages


def home(request):
    # import pdb
    # pdb.set_trace()
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'users/home.html', context)


def about(request):
    u_form = UserUpdateForm()

    return render(request, 'users/profile.html', {'u_form': u_form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account Created!')

            return redirect('blog-login')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


# def profile(request):
#     return render(request, 'users/profile.html')

# Create your views here.
