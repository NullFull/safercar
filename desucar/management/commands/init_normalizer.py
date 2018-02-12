import json
import re

from django.conf import settings
from django.core.management import BaseCommand
from desucar.models import Car
from desucar.utils import normalize


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        m = {}
        for car in Car.objects.all():
            tokens = re.split(r'[(),\W]', car.name)
            for token in tokens:
                for similar in normalize.similar_names(token):
                    m[similar] = token
        print(m)
        json.dump(m, open(settings.NORMALIZE_MAP_PATH, 'w+'))
