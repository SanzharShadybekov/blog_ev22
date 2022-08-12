from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', views.CategoryListView.as_view()),
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),

    # path('posts/', views.PostListCreateView.as_view()),
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),
    # path('posts/', views.PostView.as_view()),
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),
    # path('posts/', views.PostListView.as_view()),
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),
    # path('posts/create/', views.
    # PostCreateView.as_view()),
    # path('posts/update/<int:pk>/', views.PostUpdateView.as_view()),
    # path('posts/delete/<int:pk>/', views.PostDeleteView.as_view()),
]



