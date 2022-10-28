from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserUpdateForm, UserLoginForm
from posts.models import Post
from .models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout


class HomeView(TemplateView):
    model = Post
    template_name = 'users/home.html'
    ordering = ['-date_created']

    def get(self, request,  *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('blog-login')

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):

        context = {
            'posts': Post.objects.all()
        }

        return context


class LoginView(TemplateView):
    template_name = 'users/login.html'
    model = User
    form = UserLoginForm

    def get(self, request,  *args, **kwargs):

        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome {}'.format(email))
                return redirect('blog-home')

            else:
                messages.warning(request, 'Invalid Email or Password')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'users/logout.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('blog-login')
        logout(request)
        messages.success(request, 'You Have Logout! ')
        return redirect('blog-login')


class UpdateProfileView(TemplateView):
    template_name = 'users/profile.html'
    u_form = UserUpdateForm

    def get(self, request,  *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('blog-login')

        u_form = self.u_form(instance=request.user)
        return render(request, self.template_name, {'u_form': u_form})

    def post(self, request,  *args, **kwargs):
        u_form = self.u_form(request.POST, request.FILES,
                             instance=request.user)
        u_form.instance.email = self.request.user.email
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Account Updated! for {}'.format(
                self.request.user.email))
            return redirect('blog-dashboard')
        else:
            return render(request, self.template_name, {'u_form': u_form})


class RegisterView(TemplateView):
    """ Registers a new account. """

    template_name = 'users/register.html'
    form = UserCreationForm

    def get(self, request,  *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request,  *args, **kwargs):

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

        context = {
            "blogs": Post.objects.filter(author=self.request.user.id),
            "liked_blogs": Post.objects.filter(likes=self.request.user)
        }

        return context
