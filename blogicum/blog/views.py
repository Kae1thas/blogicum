from django.shortcuts import render



# Главная страница - список постов
def index(request):
    return render(request, 'blog/index.html', {'posts': posts[::-1]})

# Страница детального поста
def post_detail(request, id):
    post = next((p for p in posts if p['id'] == id), None)
    if not post:
        return render(request, '404.html', status=404)  # Если пост не найден
    return render(request, 'blog/detail.html', {'post': post})

# Страница категории
def category_posts(request, category_slug):
    return render(request, 'blog/category.html', {'category_slug': category_slug})
