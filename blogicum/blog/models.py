from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Category(models.Model):
    title = models.CharField("Заголовок", max_length=256)
    description = models.TextField("Описание")
    slug = models.SlugField("Идентификатор", unique=True, help_text="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.")
    is_published = models.BooleanField("Опубликовано", default=True, help_text="Снимите галочку, чтобы скрыть публикацию.")
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

class Location(models.Model):
    name = models.CharField("Название места", max_length=256)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=256)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField("Дата и время публикации", help_text="Если установить дату и время в будущем — можно делать отложенные публикации.")
    author = models.ForeignKey(User, verbose_name="Автор публикации", on_delete=models.CASCADE, related_name="posts")
    location = models.ForeignKey(Location, verbose_name="Местоположение", on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True, related_name="posts")
    is_published = models.BooleanField("Опубликовано", default=True, help_text="Снимите галочку, чтобы скрыть публикацию.")
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title
