from django.urls import path
from .views import index, post_detail, category_posts

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),  # Главная страница блога
    path('posts/<int:id>/', post_detail, name='post_detail'),  # Страница отдельного поста
    path('category/<str:category_slug>/', category_posts, name='category_posts'),  # Страница категории
]

