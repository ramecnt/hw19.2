from django.core.management import BaseCommand

from catalog.models import Product

class Fill(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        products = [
            {"name": "Огурец", "description": "Желтый", "price_per_unit": 120},
            {"name": "Огурец", "description": "Зеленый", "price_per_unit": 100},
            {"name": "Огурец", "description": "Красный", "price_per_unit": 30},
            {"name": "Огурец", "description": "Белый", "price_per_unit": 180},
        ]

        product_for_create = []
        for product in products:
            product_for_create.append(Product(**product))

        Product.objects.bulk_create(product_for_create)