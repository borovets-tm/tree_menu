from django.contrib import admin
from app_menu.models import Menu, Category


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']
