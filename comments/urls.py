from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import CreateCommentView, UpdateCommentView, CommentDeleteView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #path('', login_required(HomeView.as_view()), name='blog-home'),

    path('<int:post_id>/', CreateCommentView.as_view(),
         name='blog-comment-create'),
    path('update/<int:pk>/', UpdateCommentView.as_view(),
         name='blog-comment-update'),
    path('delete/<int:pk>', login_required(CommentDeleteView.as_view()),
         name='blog-comment-delete')
]
