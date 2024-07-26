from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    # поля таблицы
    author = models.CharField(max_length=50, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст поста')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Опубликовано',
                                      editable=False)  # Параметр 'editable' отключает возможность для редактирования
    image = models.ImageField(upload_to='posts/', null=True, verbose_name='Изображение')

    class Meta:  # Настроечный класс
        # Имя таблицы в единственном числе
        verbose_name = 'Пост'
        # Имя таблицы
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
