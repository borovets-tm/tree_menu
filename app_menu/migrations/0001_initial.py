# Generated by Django 4.2.1 on 2023-05-10 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='наименование меню')),
            ],
            options={
                'verbose_name': 'меню',
                'verbose_name_plural': 'меню',
                'db_table': 'menu',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='наименование категории')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_category', to='app_menu.category', verbose_name='родительская категория')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_category', to='app_menu.menu', verbose_name='меню')),
            ],
            options={
                'verbose_name': 'категория меню',
                'verbose_name_plural': 'категории меню',
                'db_table': 'category',
            },
        ),
    ]
