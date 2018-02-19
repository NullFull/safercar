from datetime import date
from django.shortcuts import render
from desucar.models import Car, Maker
from desucar.utils.normalize import normalize_name, is_year


def index(request):
    return render(request, 'index.html', dict(
        makers=Maker.objects.all(),
        cars=Car.objects.all(),
    ))


def detail(request, maker_name, car_name, car_year, car_code):
    car = Car.objects.get(code=car_code)

    defects = car.defects.all()

    stats = {
        '리콜': sum(1 for x in defects if x.kind == 'RC'),
        '무상수리': sum(1 for x in defects if x.kind == 'FF'),
    }

    return render(request, 'detail.html', dict(
        car=car,
        defects=defects,
        stats=stats,
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
