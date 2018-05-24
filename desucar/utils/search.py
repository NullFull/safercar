import json
from datetime import date

import pygtrie

from desucar.models import Maker, Car
from desucar.utils import normalize


def tokenize(s):
    s = s.replace('-', ' ')
    s = s.replace('(', ' ')
    s = s.replace(')', ' ')
    s = s.replace('/', ' ')
    s = s.replace('자동차', ' 자동차')
    return s.split()


class SearchSourceBuilder(object):
    def __init__(self):
        self._car_pairs = set()
        self._maker_pairs = set()

    def _build_car_pairs(self):
        for car in Car.objects.all():
            for token in tokenize(car.name):
                for kw in normalize.similar_names(token):
                    self._car_pairs.add((kw.upper(), car.id))
            for token in tokenize(car.search_keywords):
                for kw in normalize.similar_names(token):
                    self._car_pairs.add((kw.upper(), car.id))

    def _build_maker_pairs(self):
        for maker in Maker.objects.all():
            for token in tokenize(maker.name):
                for kw in normalize.similar_names(token):
                    self._maker_pairs.add((kw.upper(), maker.id))

    def build(self):
        self._build_car_pairs()
        self._build_maker_pairs()
        return {
            'cars': list(self._car_pairs),
            'makers': list(self._maker_pairs),
        }


class Searcher(object):
    def __init__(self, makers, cars):
        self._makers_trie = pygtrie.CharTrie()
        self._cars_trie = pygtrie.CharTrie()

        for kw, maker in makers:
            if kw not in self._makers_trie:
                self._makers_trie[kw] = set()
            self._makers_trie[kw].add(maker)

        for kw, car in cars:
            if kw not in self._cars_trie:
                self._cars_trie[kw] = set()
            self._cars_trie[kw].add(car)

    def search(self, q):
        maker_ids = set()
        car_ids = set()
        year = None

        for token in tokenize(q):
            token = token.upper()
            if len(token) == 4 and token.isdigit() and token[:2] in ['20', '19']:
                year = int(token)

            try:
                for key in self._makers_trie.keys(token):
                    maker_ids = maker_ids.union(self._makers_trie.get(key))
            except KeyError as e:
                pass

            try:
                for key in self._cars_trie.keys(token):
                    new_ids = self._cars_trie.get(key)
                    commons = car_ids.intersection(new_ids)
                    if len(commons) > 0:
                        car_ids = commons
                    else:
                        car_ids = car_ids.union(new_ids)
            except KeyError as e:
                pass

        makers = list(Maker.objects.filter(id__in=maker_ids).all())
        car_query = Car.objects.filter(id__in=car_ids)
        if year:
            car_query = car_query.filter(make_start__lte=date(year + 1, 1, 1))
            car_query = car_query.filter(make_end__gte=date(year - 1, 1, 1)) | car_query.filter(make_end__isnull=True)
        if len(makers) > 0:
            car_query = car_query.filter(maker__id__in=maker_ids)

        cars = list(car_query.order_by('id').all())

        if len(cars) < 1 and len(makers) > 0:
            for maker in makers:
                cars += maker.cars.all()

        return makers, cars, year
