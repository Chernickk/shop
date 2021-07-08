import json
import os
import re
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from mainapp import models


JSON_PATH = 'mainapp/jsons'

MODELS_LIST = {
                'productcategory': models.ProductCategory,
                'product': models.Product
            }
FOREIGN_KEYS = {
    'category': models.ProductCategory
}


def load_json(filename):
    with open(os.path.join(JSON_PATH, f'{filename}.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def fix_foreign_keys(fields):
    """make model object from pk in json"""
    for key in fields:
        if key in FOREIGN_KEYS.keys():
            fk_object = FOREIGN_KEYS[key].objects.get(pk=fields[key])
            fields[key] = fk_object


class Command(BaseCommand):
    help = 'Create and save objects from JSON'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='?', type=str)

    def handle(self, *args, **options):

        # Drop products and products category
        models.Product.objects.all().delete()
        models.ProductCategory.objects.all().delete()

        if options['filename']:
            jsons = load_json(options['filename'])

            for obj in jsons:
                model_name = re.search("(\.)(\w+)", obj['model']).group(2)
                if model_name:
                    model = MODELS_LIST[model_name]

                    fields = obj['fields']
                    fix_foreign_keys(fields)

                    new_object = model(**fields)
                    new_object.save()

        else:
            raise CommandError('You forget to enter a filename!')
