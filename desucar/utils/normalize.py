import json
import re
from collections import defaultdict
from itertools import product
import hgtk
import os
from django.conf import settings

similar_초성s = [
    {'ㅆ', 'ㅅ'},
]
similar_중성s = [
    {'ㅔ', 'ㅐ'},
    {'ㅓ', 'ㅕ', 'ㅗ'},
]
similar_종성s = [

]


def get_contained_set(sets, item):
    for s in sets:
        if item in s:
            return s
    return {item}


def similar_names(name):
    # TODO : simplify
    print(name)

    if not hgtk.checker.is_hangul(name):
        yield name
        return

    replaces = defaultdict(list)
    for i, char in enumerate(name):
        초성, 중성, 종성 = hgtk.letter.decompose(char)

        aa = get_contained_set(similar_초성s, 초성)
        bb = get_contained_set(similar_중성s, 중성)
        cc = get_contained_set(similar_종성s, 종성)

        for a, b, c in product(aa, bb, cc):
            new_char = hgtk.letter.compose(a, b, c)
            replaces[i].append(new_char)

    for x in product(*replaces.values()):
        yield ''.join(x)


def is_year(s):
    return s.isdigit and len(s) == 4


def separate_year(keyword):
    d4 = re.compile('\d{4}')
    l = keyword.split(' ')
    yyyy = d4.search(keyword)
    if yyyy:
        l.remove(yyyy.group())
        return [int(yyyy.group()), ' '.join(l)]
    else:
        return [None, ' '.join(l)]


def generate_map(names):
    m = {}
    for name in names:
        for new_name in similar_names(name):
            m[new_name] = name
    return m


def load_normalize_map():
    return json.load(open(settings.NORMALIZE_MAP_PATH)) if os.path.exists(settings.NORMALIZE_MAP_PATH) else {}


normalize_map = load_normalize_map()


def normalize_name(s):
    return normalize_map.get(s, s)

