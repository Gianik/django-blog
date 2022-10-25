from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    CreateCommentView,
                    UpdateCommentView,
                    CommentDeleteView,
                    LikeunlikeView)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('', login_required(HomeView.as_view()), name='blog-home'),
    path('<int:pk>/', login_required(PostDetailView.as_view()), name='blog-detail'),
    path('new/', PostCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update/', login_required(PostUpdateView.as_view()),
         name='blog-update'),
    path('<int:pk>/delete/', login_required(PostDeleteView.as_view()),
         name='blog-delete'),
    path('comment/<int:post_id>/', CreateCommentView.as_view(),
         name='blog-comment-create'),
    path('comment/update/<int:pk>/', UpdateCommentView.as_view(),
         name='blog-comment-update'),
    path('comment/delete/<int:pk>', login_required(CommentDeleteView.as_view()),
         name='blog-comment-delete'),
    #     path('like/change/<int:pk>', login_required(LikeunlikeView.as_view()),
    #     name='blog-likeunlike')
]
