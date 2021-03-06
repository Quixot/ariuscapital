# Generated by Django 4.0.1 on 2022-02-16 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project_access',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '1. Доступ к проекту',
            },
        ),
        migrations.CreateModel(
            name='Project_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '2. Тип проекта',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='проект')),
                ('deal_sence', models.TextField(verbose_name='суть')),
                ('deal_why', models.TextField(verbose_name='почему')),
                ('image', models.ImageField(null=True, upload_to='images/', verbose_name='фото')),
                ('price', models.PositiveIntegerField(verbose_name='сумма usd.')),
                ('investment_term', models.PositiveIntegerField(verbose_name='срок мес.')),
                ('income', models.PositiveIntegerField(verbose_name='% доходности')),
                ('address', models.CharField(max_length=512, verbose_name='адрес')),
                ('start', models.DateTimeField(verbose_name='Старт')),
                ('end', models.DateTimeField(verbose_name='Финиш')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True)),
                ('access', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project_access', verbose_name='Тип')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project_type', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'проекты',
                'verbose_name_plural': 'проекты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment', models.IntegerField(verbose_name='Размер инвестиции')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.project', verbose_name='Проект')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'инвестиции',
                'verbose_name_plural': 'инвестиции',
            },
        ),
    ]
