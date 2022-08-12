from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=255
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True
        )

    def __str__(self) -> str:
        return f'{self.name} --> {self.parent}' if self.parent else self.name


class Post(models.Model):
    title = models.CharField(
        max_length=255, unique=True,
        verbose_name="Название")
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User',
        related_name="posts",
        on_delete=models.CASCADE)
    category = models.ForeignKey(Category, 
        on_delete=models.SET_NULL, 
        related_name='posts', null=True)
    preview = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.owner} - {self.title}'


    class Meta:
        ordering = ('created_at',)
        verbose_name = "Посты"
        verbose_name_plural = "Пост"


class PostImages(models.Model):
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    
    @staticmethod
    def generate_name():
        from random import randint
        return 'image' + str(randint(100_000,999_999))
    
    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImages, self).save(*args, **kwargs)


class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} -> {self.post} -> {self.created_at}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['post', 'owner']


class Favorites(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['post', 'owner']

