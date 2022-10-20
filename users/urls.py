from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('register/', views.register, name="blog-register"),
    # path('profile/', views.profile, name="blog-profile"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
         name="blog-login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name="blog-logout"),
    #path('api-auth/', include('rest_framework.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
