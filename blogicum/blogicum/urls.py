from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),  # Подключаем blog с namespace
    path('pages/', include('pages.urls', namespace='pages')),  # Подключаем pages\
        path('path/to/main.css', TemplateView.as_view(
        template_name='main.css',
        content_type='text/css')
    ),
]
