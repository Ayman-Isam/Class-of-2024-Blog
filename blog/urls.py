from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, LikeView, PostCommentCreateView, PostCommentUpdateView, PostCommentDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>/', LikeView, name='like-post'),  
    path('about/', views.about, name='blog-about'),
    path('post/<int:post_pk>/comment/', PostCommentCreateView.as_view(), name='post-comment'),
    path('post/<int:post_pk>/comment-update/<int:pk>/', PostCommentUpdateView.as_view(), name='post-comment-update'),
    path('post/<int:post_pk>/comment-delete/<int:pk>/', PostCommentDeleteView.as_view(), name='post-comment-delete'),
    path('search/', views.search, name='search-post'),
]
