from django.db import models


class Menu(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='наименование меню'
    )

    class Meta:
        db_table = 'menu'
        verbose_name = 'меню'
        verbose_name_plural = 'меню'

    def __str__(self):
        return self.title


class Category(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='menu_category',
        verbose_name='меню'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='parent_category',
        verbose_name='родительская категория',
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=50,
        verbose_name='наименование категории'
    )

    class Meta:
        db_table = 'category'
        verbose_name = 'категория меню'
        verbose_name_plural = 'категории меню'

    def __str__(self):
        if self.category:
            return f'{self.category} | {self.title}'
        else:
            return f'{self.menu} | {self.title}'
