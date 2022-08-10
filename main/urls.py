from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('acoount/register/', views.UserRegistrationView.as_view()),

    path('categories/', views.CategoryListView.as_view()),

    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('posts/create/', views.
    PostCreateView.as_view()),
    path('posts/update/<int:pk>/', views.PostUpdateView.as_view()),
    path('posts/delete/<int:pk>/', views.PostDeleteView.as_view()),

    path('apiview/posts/', views.PostView.as_view()),
]



