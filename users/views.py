from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from myblog.settings import LOGIN_REDIRECT_URL
from .forms import UserRegistrationForm


def register(request):
    # если нажали кнопку регистрации (метод POST)
    if request.method == 'POST':
        # создаем объект с данными из запроса
        user_form = UserRegistrationForm(request.POST)
        # Валидация формы (правильность введенных данных)
        if user_form.is_valid():
            # Создание объекта с полями формы (без сохранения в БД)
            new_user = user_form.save(commit=False)
            # Хеширование пароля пользователя
            new_user.set_password(user_form.cleaned_data['password'])  # Хеширование пароля
            # Сохранение пользователя в БД
            new_user.save()  # по умолчанию commit=True
            context = {'title': 'Успешная регистрация', 'new_user': new_user}
            return render(request, template_name='users/register_done.html', context=context)

    # Если метод GET - отрисовка страницы регистрации
    user_form = UserRegistrationForm()
    context = {'title': 'Регистрация', 'register_form': user_form}
    return render(request, template_name='users/register.html', context=context)


def log_in(request):
    # Создание формы аутентификации
    form = AuthenticationForm(request, request.POST)
    # Проверка формы
    if form.is_valid():
        # Получения логина и пароля из формы
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # Аунтификация пользователя (проверка наличия пользователя и пароля)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Авторизация пользователя (проверка прав доступа)
            login(request, user)
            # Получение дальнейшего маршрута после авторизации (next - путь, откуда пришел пользователь)
            url = request.GET.get('next', LOGIN_REDIRECT_URL)
            return redirect(url)
    context = {'form': form}
    return render(request, template_name='users/login.html', context=context)


def log_out(request):
    logout(request)
    return redirect('blog:index')


def user_detail(request, pk):
    pass


def change_password(request, pk):
    pass
