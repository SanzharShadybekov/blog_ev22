from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserListView.as_view()),
    path('acoount/register/', views.UserRegistrationView.as_view()),
    path('posts/', views.PostListView.as_view()),
]




