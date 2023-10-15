from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    name = models.CharField('Имя', max_length=300)
    birthday = models.DateField('Дата рождения')
    bio = models.CharField('Краткая биография', max_length=3000)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField('Название', max_length=500)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='Автор',
    )
    publish_year = models.PositiveSmallIntegerField('Год издания')
    synopsys = models.CharField('Краткое описание', max_length=2000)
    cover = models.ImageField('Обложка', upload_to='covers')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        unique_together = [['name', 'author', 'publish_year']]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("book", kwargs={"pk": self.pk})
    
    
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Книга',
    )
    text = models.CharField('Текст', max_length=200)
    published = models.DateTimeField('Опубликован', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
