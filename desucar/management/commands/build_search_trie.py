import json
from django.conf import settings
from django.core.management import BaseCommand
from desucar.utils.search import SearchSourceBuilder


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = SearchSourceBuilder().build()
        json.dump(data, open(settings.SEARCH_MAP_PATH, 'w+'))
