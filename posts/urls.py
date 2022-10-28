from django.urls import path
from .views import (PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    CreateCommentView,
                    UpdateCommentView,
                    CommentDeleteView,
                    LikeunlikeView)
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('<int:pk>/', PostDetailView.as_view(), name='blog-detail'),
    path('new/', PostCreateView.as_view(), name='blog-create'),
    path('update/<int:pk>', login_required(PostUpdateView.as_view()),
         name='blog-update'),
    path('delete/<int:pk>', login_required(PostDeleteView.as_view()),
         name='blog-delete'),
    path('comment/<int:post_id>/', CreateCommentView.as_view(),
         name='blog-comment-create'),
    path('comment/update/<int:pk>/', UpdateCommentView.as_view(),
         name='blog-comment-update'),
    path('comment/delete/<int:pk>', login_required(CommentDeleteView.as_view()),
         name='blog-comment-delete'),
    path('like/change/<int:pk>', login_required(LikeunlikeView.as_view()),
         name='blog-likeunlike')
]
