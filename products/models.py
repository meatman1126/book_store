from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='カテゴリー名')
    english_name = models.CharField(max_length=100, verbose_name='カテゴリー名（英語）')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='スラッグ')
    description = models.TextField(blank=True, verbose_name='説明')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリー')
    name = models.CharField(max_length=200, verbose_name='商品名')
    english_name = models.CharField(max_length=200, verbose_name='商品名（英語）')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='スラッグ')
    description = models.TextField(blank=True, verbose_name='説明')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='価格')
    stock = models.PositiveIntegerField(default=0, verbose_name='在庫数')
    available = models.BooleanField(default=True, verbose_name='販売中')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.english_name)
        super().save(*args, **kwargs)
