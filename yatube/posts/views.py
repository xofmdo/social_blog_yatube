from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Follow
from .utils import get_page_obj

User = get_user_model()


@cache_page(20)
def index(request: HttpRequest) -> HttpResponse:
    """Отображение главной страницы"""
    posts = Post.objects.select_related('author', 'group').all()
    page_obj = get_page_obj(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context=context)


def group_list(request: HttpRequest, slug: str) -> HttpResponse:
    """Отображение сгруппированных постов"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').all()
    context = {
        'group': group,
        'page_obj': get_page_obj(request, posts),
    }
    return render(request, 'posts/group_list.html', context=context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """ Отображение профиля пользователя"""
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')
    following = request.user.is_authenticated and (Follow.objects.filter(
        user=request.user, author=author).exists())
    context = {
        'author': author,
        'page_obj': get_page_obj(request, posts),
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """ Детали поста"""
    group = Post.objects.select_related('group')
    post = get_object_or_404(group, id=post_id)
    comments = post.comments.select_related('author')
    comments_form = CommentForm(request.POST)
    context = {
        'post': post,
        'comments': comments,
        'form': comments_form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    """ Создание поста"""
    form = PostForm(request.POST, files=request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)

    return render(request, 'posts/create_post.html',
                  {'form': form, 'username': request.user})


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    """ Редактирование поста"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html',
                  context=context)


@login_required
def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    """Добавление комментария к посту"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request: HttpRequest) -> HttpResponse:
    """Возвращает страницу с постами авторов, на которых подписан
        пользователь."""
    posts = Post.objects.filter(author__following__user=request.user)
    context = {
        'page_obj': get_page_obj(request, posts),
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request: HttpRequest, username: str) -> HttpResponse:
    """Добавление подписки на автора."""
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request: HttpRequest, username: str) -> HttpResponse:
    """Удаление автора из подписок."""
    Follow.objects.filter(
        user=request.user, author__username=username).delete()
    return redirect('posts:profile', username)
