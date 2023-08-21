import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

data_path = f'{settings.BASE_DIR}/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(data_path + 'ingredients.json', 'r',
                  encoding='UTF-8') as file:
            ingredients = json.load(file)
            for ingredient in ingredients:
                Ingredient.objects.get_or_create(**ingredient)

        with open(data_path + 'tags.json', 'r',
                  encoding='UTF-8') as file:
            tags = json.load(file)
            for tag in tags:
                Tag.objects.get_or_create(**tag)
