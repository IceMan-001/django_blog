from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import PostForm
from .models import Post

"""
Представление на функциях и классах
FBV - Function base views
CBV - Class bases views
"""


def root(request):
    posts = Post.objects.all()
    context = {
        'title': 'Посты',
        'posts': posts
    }
    return render(request, template_name='blog/index.html', context=context)


def index(request):
    posts = Post.objects.all()
    context = {
        'title': 'Посты',
        'posts': posts
    }
    return render(request, template_name='blog/index.html', context=context)


def about(request):
    context = {
        'name': 'Дмитрий',
        'lastname': 'Горин',
        'email': 'd.gorin@yandex.ru',
        'title': 'О сайте'
    }
    return render(request, template_name='blog/about.html', context=context)


def contacts(request):
    context = {
        'name': 'Тестовый сайт на Django',
        'email': 'd.test@yandex.ru',
        'title': 'Здесь будут контакты'
    }
    return render(request, template_name='blog/contacts.html', context=context)


def send_data(request):
    data = {'name': 'Elena', 'age': 36}
    return JsonResponse(data=data)


@login_required
def add_post(request):
    if request.method == 'GET':
        form = PostForm(author=request.user)
        context = {
            'form': form,
            'title': 'Добавление поста'
        }
        return render(request, template_name='blog/add_post.html', context=context)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():
            # instance = form.save(commit=False)  # объект модели (можно изменить перед записью в таблицу)
            # instance.title = 'Миша'
            # post = Post()
            # post.author = form.cleaned_data['author']
            # post.title = form.cleaned_data['title']
            # post.text = form.cleaned_data['text']
            # post.image = form.cleaned_data['image']
            # post.save()
            form.save(commit=True)

        return index(request)


def post_list(request):
    # Получаем все объекты модели Post
    # сортируем по убыванию
    posts = Post.objects.all().order_by('-created_at')
    # показываем по 3 поста на странице
    # получаем номер страницы из url
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    # получаем объекты для текущей страницы
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Посты',
        'page_obj': page_obj
    }
    return render(request, template_name='blog/posts.html', context=context)


def post_list_in_table(request):  # Посты в виде таблицы
    # Получаем все объекты модели Post
    posts = Post.objects.all()
    context = {
        'title': 'Посты',
        'posts': posts
    }
    return render(request, template_name='blog/posts_in_table.html', context=context)


def post_detail(request, slug):
    # получаем объект с заданным первичным ключом
    post = get_object_or_404(Post, slug=slug)
    # post = Post.objects.get(pk=pk)
    context = {
        'title': 'Информация о посте',
        'post': post
    }

    return render(request, template_name='blog/post_detail.html', context=context)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)  # получить объект по ключу
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            return post_list(request)

    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'title': 'Редактировать пост'
    }
    return render(request, template_name='blog/post_edit.html', context=context)


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)  # получить объект по ключу
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, template_name="blog/post_delete.html", context={'post': post})


def product_search(request):
    query = request.GET.get('query')
    query_text = Q(title__contains=query) & Q(title__icontains=query)

    page_obj = Post.objects.filter(query_text)

    context = { 'page_obj': page_obj}

    return render(request, template_name="blog/posts.html", context=context)


def page_not_found(request, exception):
    return render(request, template_name='blog/404.html', status=404)


def forbidden(request, exception):
    return render(request, template_name='blog/403.html', status=403)


def server_error(request):
    return render(request, template_name='blog/500.html', status=500)
