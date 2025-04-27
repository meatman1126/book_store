from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'english_name', 'slug', 'description')
    prepopulated_fields = {'slug': ('english_name',)}
    search_fields = ('name', 'english_name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'english_name', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at', 'category')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('english_name',)}
    search_fields = ('name', 'english_name', 'description')
    date_hierarchy = 'created_at'
