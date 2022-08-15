from django.db import connection
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAuthor, IsAccountOwner
from . import serializers
from .models import Category, Post, Comment, Like, Favorites

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


class StandartResultsPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserListSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAccountOwner)
    serializer_class = serializers.UserSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('owner', 'category',)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', 'owner')
    search_fields = ('title',)
    pagination_class = StandartResultsPagination

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print(f'Запросов в базу данных: {len(connection.queries)}')
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return serializers.PostSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        else:
            return serializers.PostListSerializer

    def get_permissions(self):
        #Создавать посты может залогинкнный юзер
        if self.action in ('create', 'add_to_liked', 'remove_from_liked', 'favorite_action'):
            return [permissions.IsAuthenticated()]
        #Изменять и удалять может только автор поста
        elif self.action in ('update', 'partial_update', 'destroy', 'get_likes'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        # Просматривать могут все
        else:
            return [permissions.AllowAny(),]
    
    # api/v1/posts/<id>/comments/
    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)
    
    # api/v1/posts/<id>/add_to_liked/
    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        post = self.get_object()
        if request.user.liked.filter(post=post).exists():
            # request.user.liked.filter(post=post).delete()
            return Response('Вы уже лайкали этот пост!', status=400)
        Like.objects.create(post=post, owner=request.user)
        return Response('Вы поставили лайк!', status=201)
    
    # api/v1/posts/<id>/remove_from_liked/
    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        post = self.get_object()
        if not request.user.liked.filter(post=post).exists():
            return Response('Вы не лайкали этот пост!', status=400)
        request.user.liked.filter(post=post).delete()
        return Response('Ваш лайк удален!', status=204)

    # api/v1/posts/<id>/get_likes/
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)
    
    # api/v1/posts/<id>/favorite_action/
    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        post = self.get_object()
        if request.user.favorites.filter(post=post).exists():
            request.user.favorites.filter(post=post).delete()
            return Response('Убрали из избранных!', status=204)
        Favorites.objects.create(post=post, owner=request.user)
        return Response('Добавлено в избранное!', status=201)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)




# Class based view(APIView)
# class PostView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = serializers.PostListSerializer(posts, many=True).data
#         return Response(serializer)
    
#     def post(self, request):
#         serializer = serializers.PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)


# class PostDetailView(APIView):
#     @staticmethod
#     def get_object(pk):
#         try:
#             post = Post.objects.get(pk=pk)
#             return post
#         except Post.DoesNotExist:
#             return False

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         if not post:
#             content = {'error': 'Invalid id!'}
#             return Response(content, status=HTTP_404_NOT_FOUND)

#         serializer = serializers.PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         post = self.get_object(pk)
#         if not post:
#             content = {'error': 'Invalid id!'}
#             return Response(content, status=HTTP_404_NOT_FOUND)

#         serializer = serializers.PostCreateSerializer(post,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=404)
    
#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         if not post:
#             content = {'error': 'Invalid id!'}
#             return Response(content, status=HTTP_404_NOT_FOUND)
        
#         if request.user == post.owner:
#             post.delete()
#             return Response('Deleted', status=204)
#         return Response('Permission denied', status=403)


# function based view
# @api_view(['GET'])
# def posts_list(request): 
#     posts = Post.objects.all()
#     serializer = serializers.PostSerializer(posts, many=True)
#     return Response(serializer.data)

# CRUD(CREATE, RETRIEVE, UPDATE, DELETE)
# generics

# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
    
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return serializers.PostListSerializer
#         return serializers.PostCreateSerializer
    
#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return (permissions.IsAuthenticated(),)
#         return (permissions.AllowAny(),)
    
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
    

# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
    
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         return serializers.PostSerializer
    
#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH', 'DELETE'):
#             return (permissions.IsAuthenticated(), IsAuthor())
#         return (permissions.AllowAny(),)

# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostListSerializer

# class PostCreateView(generics.CreateAPIView):
#     serializer_class = serializers.PostCreateSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def perform_create(self, serializer):
#         # print(self.request.user,'!!!!!!!!!!!!!!!!')
#         serializer.save(owner=self.request.user)


# class PostDetailView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer


# class PostUpdateView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#     permission_classes = (permissions.IsAuthenticated, IsAuthor)


# class PostDeleteView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticated, IsAuthor)



