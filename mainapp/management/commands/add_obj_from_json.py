from django.core.management.base import BaseCommand, CommandError
from mainapp import models
import json


class Command(BaseCommand):
    """example json:
    {"1":
        {"name": "Табуретка",
        "price": 1200,
        "quantity": 10,
        "category": "Классика"},
    "2":
        {"name": "Шкаф",
        "price": 500,
        "quantity": 30,
        "category": "Модерн"}
    }"""

    help = 'Create and save objects from JSON'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['path']:
            with open(options['path'], 'r') as f:
                json_file = json.load(f)
            for el in json_file.values():
                category = models.ProductCategory.objects.get(name=el.pop('category'))
                product = models.Product(**el, category=category)
                product.save()
        else:
            print('please enter a path')