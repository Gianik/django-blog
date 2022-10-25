from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users.views import RegisterView, HomeView, UpdateProfileView, DashboardView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='blog-home'),
    path('about/', login_required(UpdateProfileView.as_view()), name='blog-about'),
    path('register/', RegisterView.as_view(), name="blog-register"),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
         name="blog-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name="blog-logout"),
    path('dashboard/', DashboardView.as_view(),
         name="blog-dashboard"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
