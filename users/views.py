from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserCreationForm, UserUpdateForm
from posts.models import Post
from django.contrib import messages
from django.views.generic import TemplateView


# def home(request):
#     # import pdb
#     # pdb.set_trace()
#     context = {
#         'posts': Post.objects.all(),
#     }
#     return render(request, 'users/home.html', context)

class HomeView(TemplateView):
    #     # import pdb
    #     # pdb.set_trace()
    template_name = 'users/home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'posts': Post.objects.all(),
        }
        return render(request, self.template_name, context)


def about(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user)

    else:
        u_form = UserUpdateForm(instance=request.user)

    # if u_form.is_valid():

    return render(request, 'users/profile.html', {'u_form': u_form})


class RegisterView(TemplateView):
    """ Registers a new account. """

    template_name = 'users/register.html'
    form = UserCreationForm

    def get(self, request,  *args, **kwargs):
        context = {}  # dictionary
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):
        import pdb
        pdb.set_trace()
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account Created! for {}'.format(email))
            return redirect('blog-login')
        else:
            return render(request, self.template_name, {'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             messages.success(request, f'Account Created!')

#             return redirect('blog-login')
#     else:
#         form = UserCreationForm()

#     return render(request, 'users/register.html', {'form': form})


# def profile(request):
#     return render(request, 'users/profile.html')

# Create your views here.
