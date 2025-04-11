from django.core.cache import cache

from catalog.models import Category
from djangoProject import settings


def cached_categories():
    if settings.CACHE_ENABLED:
        key = 'categories_list'
        categories = cache.get(key)
        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories)
    else:
        categories = Category.objects.all()
    return categories
