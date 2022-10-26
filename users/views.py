from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm

from .forms import UserCreationForm, UserUpdateForm
from posts.models import Post
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(TemplateView):
    #     # import pdb
    #     # pdb.set_trace()

    model = Post
    template_name = 'users/home.html'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):

        context = super(HomeView, self).get_context_data()
        # this contain the object that the view is operating upon

        context['posts'] = Post.objects.all()

        return context


class UpdateProfileView(TemplateView):
    template_name = 'users/profile.html'
    u_form = UserUpdateForm

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

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
            return redirect('blog-dashboard')
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


class DashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):

        context = super(TemplateView, self).get_context_data()
        # this contain the object that the view is operating upon
        # user_object = self.object
        # context['object'] = user_object

        context['blogs'] = Post.objects.filter(author=self.request.user.id)
        context['liked_blogs'] = Post.objects.filter(likes=self.request.user)

        return context
