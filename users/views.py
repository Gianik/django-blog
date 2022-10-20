from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserCreationForm, UserUpdateForm
from posts.models import Post
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    #     # import pdb
    #     # pdb.set_trace()
    template_name = 'users/home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'posts': Post.objects.all(),
        }
        return render(request, self.template_name, context)


class UpdateProfileView(TemplateView):
    template_name = 'users/profile.html'
    u_form = UserUpdateForm

    def get(self, request,  *args, **kwargs):
        context = {}
        u_form = self.u_form(instance=request.user)
        return render(request, self.template_name, {'u_form': u_form})

    def post(self, request,  *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        u_form = self.u_form(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            email = u_form.cleaned_data.get('email')
            messages.success(request, 'Account Updated! for {}'.format(email))
            return redirect('blog-about')
        else:
            return render(request, self.template_name, {'u_form': u_form})


class RegisterView(TemplateView):
    """ Registers a new account. """

    template_name = 'users/register.html'
    form = UserCreationForm

    def get(self, request,  *args, **kwargs):
        context = {}  # dictionary
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account Created! for {}'.format(email))
            return redirect('blog-login')
        else:
            return render(request, self.template_name, {'form': form})
