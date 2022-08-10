from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .permissions import IsAuthor
from . import serializers
from .models import Category, Post
from rest_framework.views import APIView
from rest_framework.response import Response

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


# Class based view(APIView)
class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = serializers.PostSerializer(posts, many=True).data
        return Response(serializer)


# function based view
# @api_view(['GET'])
# def posts_list(request): 
#     posts = Post.objects.all()
#     serializer = serializers.PostSerializer(posts, many=True)
#     return Response(serializer.data)

# CRUD(CREATE, RETRIEVE, UPDATE, DELETE)
# generics
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostListSerializer

class PostCreateView(generics.CreateAPIView):
    serializer_class = serializers.PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        # print(self.request.user,'!!!!!!!!!!!!!!!!')
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)



