from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, PostImages, Comment, Like, Favorites

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,
                                     write_only=True,
                                     required=True)
    password2 = serializers.CharField(min_length=6,
                                      write_only=True,
                                      required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError(
                'Passwords didn\'t match')
        return attrs

    @staticmethod
    def validate_first_name(value):
        if not value.istitle():
            raise serializers.ValidationError(
                'Name must start with uppercase!'
            )
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name'))
        user.set_password(validated_data['password'])
        user.save()
        return user


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('post',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post'] = PostListSerializer(instance.post).data
        return repr


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['favorites'] = FavoritesSerializer(instance.favorites.all(), many=True).data
        return repr

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username')
    category = serializers.ReadOnlyField(
        source='category.name')
    images = PostImageSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True) #1 способ!

    class Meta:
        model = Post
        fields = '__all__'

    def is_liked(self, post):
        user = self.context.get('request').user
        return user.liked.filter(post=post).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # repr['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        return repr


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'preview')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        created_post = Post.objects.create(**validated_data)
        images_data = request.FILES
        images_object = [PostImages(post=created_post, image=image) for image in images_data.getlist('images')]
        PostImages.objects.bulk_create(images_object)
        return created_post


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source=
    'owner.username')
    
    class Meta:
        model = Like
        fields = ('owner',)
