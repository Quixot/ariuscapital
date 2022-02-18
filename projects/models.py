from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe
from user.models import User


class Project_access(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '1. Доступ к проекту'


class Project_type(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2. Тип проекта'


class Project(models.Model):
    title = models.CharField(verbose_name='проект', max_length=255)
    deal_sence = models.TextField(verbose_name='суть')
    deal_why = models.TextField(verbose_name='почему')
    image = models.ImageField(verbose_name='фото', upload_to='images/', null=True)
    price = models.PositiveIntegerField(verbose_name='сумма usd.')
    investment_term = models.PositiveIntegerField(verbose_name='срок мес.')
    income = models.PositiveIntegerField(verbose_name='% доходности')
    address = models.CharField(verbose_name='адрес', max_length=512)
    access = models.ForeignKey(Project_access, on_delete=models.CASCADE, verbose_name='Статус')
    type = models.ForeignKey(Project_type, on_delete=models.CASCADE, verbose_name='Тип')
    start = models.DateTimeField(verbose_name='Старт', auto_now=False, auto_now_add=False)
    end = models.DateTimeField(verbose_name='Финиш', auto_now=False, auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    published = models.BooleanField(default=True)

    # temp_persend = models.IntegerField(default=50)

    def __str__(self):
        return self.title

    def image_prev(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.image.url))

    image_prev.short_description = 'Фото'

    @property
    def image_path(self):
        if self.image:
            return self.image.url
        else:
            return ''

    @property
    def days_left(self):
        return self.end.date() - self.start.date()

    @property
    def total_sum(self):
        return sum([item.investment for item in Order.objects.filter(project=self.id)])

    @property
    def total_perсend(self):
        return self.total_sum*100/self.price

    class Meta:
        verbose_name = 'проекты'
        verbose_name_plural = 'проекты'


class Order(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name='Проект')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    investment = models.IntegerField(verbose_name='Размер инвестиции')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True, auto_now=False)

    def __str__(self):
        return ('%s - %s' % (self.user.email, self.project.title))

    class Meta:
        verbose_name = 'инвестиции'
        verbose_name_plural = 'инвестиции'
