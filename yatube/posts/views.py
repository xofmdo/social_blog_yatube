from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

from .forms import PostForm
from .models import Group, Post, User
from .utils import get_page_obj


User = get_user_model()


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
    """ Профиль пользователя"""
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author')
    context = {
        'author': author,
        'page_obj': get_page_obj(request, posts),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id) -> HttpResponse:
    """ Детали поста"""
    group = Post.objects.select_related('group')
    post = get_object_or_404(group, id=post_id)
    context = {
        'post': post,
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
    if post.author_id != request.user.id:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method != 'POST':
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html',
                      context={'form': form, 'is_edit': True})
    form = PostForm(
        request.POST,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
        'username': request.user,
    }
    return render(request, 'posts/create_post.html',
                  context=context)
