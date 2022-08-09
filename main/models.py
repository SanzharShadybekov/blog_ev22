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
