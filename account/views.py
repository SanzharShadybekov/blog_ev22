from django.shortcuts import render
from rest_auth.views import LogoutView, LoginView
from rest_framework import permissions

class CustomLogoutView(LogoutView):
    permission_classes = (
        permissions.IsAuthenticated,)

class CustomLoginView(LoginView):
    permission_classes = (permissions.AllowAny,)




    