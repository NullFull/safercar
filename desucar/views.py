from django.shortcuts import render
from desucar.models import Car, Maker, Defect


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
    q = request.GET.get('q')

    cars = Car.objects.filter(name__contains=q).all()

    return render(request, 'search.html', dict(
        q=q,
        cars=cars,
    ))
