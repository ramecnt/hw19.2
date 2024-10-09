from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class Produpi3ctAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_per_unit', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
