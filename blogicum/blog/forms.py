from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post, Page

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text',  'category', 'location', 'image', 'is_published', 'pub_date']  # Добавляем location и pub_date

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'slug', 'is_published']