from django.db import models
from django.urls import reverse


class HeadMenuModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название меню')
    slug = models.SlugField(max_length=100, unique=True,  verbose_name='Слаг')

    class Meta:
        ordering = ['id']
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu', kwargs={'menu_slug': self.slug})


class MenuItemModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название меню')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name='Элемент меню на уровень выше')
    head_menu = models.ForeignKey(to=HeadMenuModel, on_delete=models.CASCADE, null=True, related_name='menu_items',
                                  verbose_name='Ссылка на объект меню-хозяина')

    class Meta:
        ordering = ['id']
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'

    def __str__(self):
        return self.name

