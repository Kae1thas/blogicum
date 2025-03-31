from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Location(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название места')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор', help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано', help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации', help_text='Если установить дату и время в будущем — можно делать отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор публикации')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Местоположение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    image = models.ImageField(upload_to='post/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к {self.post.title}'


class Page(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор', help_text='Уникальный URL-адрес страницы.')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title