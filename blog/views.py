from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .forms import PostForm
from .models import Post


def root(request):
    return render(request, template_name='blog/index.html')


def index(request):
    return render(request, template_name='blog/index.html')


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


def add_post(request):
    if request.method == 'GET':
        form = PostForm()
        context = {
            'form': form,
            'title': 'Добавление поста'
        }
        return render(request, template_name='blog/add_post.html', context=context)

    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = Post()
            post.author = form.cleaned_data['author']
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.save()

            return index(request)


def post_list(request):
    # Получаем все объекты модели Post
    posts = Post.objects.all()
    context = {
        'title': 'Посты',
        'posts': posts
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
