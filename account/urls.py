from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view()),
    path('logout/', views.CustomLogoutView.as_view()),
]

