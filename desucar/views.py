from datetime import date
from django.shortcuts import render
from desucar.models import Car, Maker
from django.http import HttpResponse
from django.core import serializers
from desucar.utils.normalize import normalize_name, is_year


def index(request):
    return render(request, 'index.html', dict(
        makers=Maker.objects.all(),
        cars=Car.objects.all(),
    ))


def detail(request, maker_name, car_name, car_year, car_code):
    car = Car.objects.get(code=car_code)
    official_defects = car.official_defects.all()
    defects = {
        '리콜': {
            'code': 'recall',
            'items': [x for x in official_defects if x.kind == 'RC'],
        },
        '무상수리': {
            'code': 'freefix',
            'items': [x for x in official_defects if x.kind == 'FF'],
        },
        '비공식 무상수리': {
            'code': 'unofficial',
            'items': list(car.community_defects.all()),
        },
        '급발진 의심': {
            'code': 'sudden-accel',
            'items': [x for x in car.sudden_accels.all()],
        }
    }

    for key, defect in defects.items():
        defects[key]['count'] = len(defects[key]['items'])

    return render(request, 'detail.html', dict(
        car=car,
        official_defects=official_defects,
        defects=defects,
    ))


def search(request):
    q = request.GET.get('q').strip()
    tokens = q.split()

    query = Car.objects
    for token in tokens:
        if is_year(token):
            year = int(token)
            query = query.filter(make_start__lte=date(year + 1, 1, 1))
            query = query.filter(make_end__gte=date(year - 1, 1, 1)) | query.filter(make_end__isnull=True)
        else:
            token = normalize_name(token)
            query = query.filter(name__contains=token)

    return render(request, 'search.html', dict(
        q=q,
        cars=query.all(),
    ))
    

def suggest(request):
    q = request.GET.get('q').strip()
    tokens = q.split()

    query = Car.objects
    for token in tokens:
        if is_year(token):
            year = int(token)
            query = query.filter(make_start__lte=date(year + 1, 1, 1))
            query = query.filter(make_end__gte=date(year - 1, 1, 1)) | query.filter(make_end__isnull=True)
        else:
            token = normalize_name(token)
            query = query.filter(name__contains=token)
    data = serializers.serialize('json', query.all())
    return HttpResponse(data, content_type='application/json')
