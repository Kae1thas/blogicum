from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Category, Post, Comment, Page
from .forms import RegistrationForm, ProfileForm, CommentForm, PostForm, PageForm
from django.contrib.auth.models import User
from django.core.mail import send_mail  
from django.conf import settings
from django.http import Http404


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            subject = f'Новый пост: {post.title}'
            message = f'Пользователь {request.user.username} создал пост "{post.title}".'
            from_email = settings.EMAIL_HOST_USER or 'noreply@blogicum.com'
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def get_published_posts(queryset):
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )

def annotate_comments_count(queryset):
    return queryset.annotate(comment_count=Count('comments'))

def get_paginated_page(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def index(request):
    post_list = annotate_comments_count(get_published_posts(Post.objects.all())).order_by('-pub_date')
    page_obj = get_paginated_page(request, post_list)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration_form.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_published = (
        post.is_published
        and post.pub_date <= timezone.now()
        and post.category.is_published
    )
    if not is_published and post.author != request.user:
        raise Http404("Post not found or not published")
    
    comments = post.comments.all().order_by('created_at')
    form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'form': form})

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = annotate_comments_count(get_published_posts(Post.objects.filter(category=category))).order_by('-pub_date')
    page_obj = get_paginated_page(request, post_list)
    return render(request, 'blog/category.html', {'category': category, 'page_obj': page_obj})

def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=profile)
    if request.user != profile:
        post_list = get_published_posts(post_list)
    post_list = annotate_comments_count(post_list).order_by('-pub_date')
    page_obj = get_paginated_page(request, post_list)
    return render(request, 'blog/profile.html', {'profile': profile, 'page_obj': page_obj})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment.html', {'post': post, 'form': form})

@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects.filter(is_published=True)

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'blog/page_form.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'blog/page_form.html'

    def get_queryset(self):
        return Page.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:page_detail', kwargs={'slug': self.object.slug})

