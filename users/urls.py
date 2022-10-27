from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, HomeView, UpdateProfileView, DashboardView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='blog-home'),
    path('about/', UpdateProfileView.as_view(), name='blog-about'),
    path('register/', RegisterView.as_view(), name="blog-register"),
    path('login/', LoginView.as_view(), name="blog-login"),
    path('logout/', LogoutView.as_view(), name="blog-logout"),
    path('dashboard/', DashboardView.as_view(), name="blog-dashboard"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
