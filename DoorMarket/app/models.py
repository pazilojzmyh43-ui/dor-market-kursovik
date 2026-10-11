from datetime import datetime
from decimal import Decimal
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    image = models.FileField(upload_to='posts', default='temp.jpg', verbose_name="Путь к картинке")
    # Самостоятельная работа 7: автор статьи из модели User
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")

    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"


class Comment(models.Model):
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return 'Комментарий %s к %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к статьям блога"
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Categories"
        verbose_name = "категория"
        verbose_name_plural = "категории каталога"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.FileField(upload_to='products', default='temp.jpg', verbose_name="Путь к картинке")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Products"
        verbose_name = "товар"
        verbose_name_plural = "товары каталога"
        ordering = ["name"]


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В работе'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменён'),
    )
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    created = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказу")

    def total(self):
        amount = Decimal('0')
        for line in self.lines.all():
            amount += line.price * line.quantity
        return amount

    def __str__(self):
        return 'Заказ №%s' % self.id

    class Meta:
        db_table = "Orders"
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        ordering = ["-created"]


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines', verbose_name="Заказ")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Товар")
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def line_sum(self):
        return self.price * self.quantity

    def __str__(self):
        return '%s × %s' % (self.name, self.quantity)

    class Meta:
        db_table = "OrderLines"
        verbose_name = "строка заказа"
        verbose_name_plural = "строки заказа"


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderLine)
