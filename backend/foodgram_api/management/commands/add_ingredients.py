import csv

from api.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Заполняет БД ингредиентами'

    def handle(self, *args, **options):
        for row in csv.DictReader(open('static/data/ingredients.csv',
                                       encoding='UTF-8')):
            Ingredient.objects.get_or_create(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
