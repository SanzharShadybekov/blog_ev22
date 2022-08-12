from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .permissions import IsAuthor
from . import serializers
from .models import Category, Post, Comment
from rest_framework.viewsets import ModelViewSet


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


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

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
        if self.action in ('create',):
            return [permissions.IsAuthenticated()]
        #Изменять и удалять может только автор поста
        elif self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        # Просматривать могут все
        else:
            return [permissions.AllowAny(),]


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



