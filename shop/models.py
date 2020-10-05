from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    """Категории товаров"""
    name = models.CharField(max_length=150, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=150, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='В наличие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
