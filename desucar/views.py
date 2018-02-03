from django.shortcuts import render
from desucar.models import Car, Maker, Revision, Defect


def index(request):
    return render(request, 'index.html', dict(
        makers=Maker.objects.all(),
        cars=Car.objects.all(),
    ))


def detail(request, maker, car, year):
    revision = Revision.objects.get(car__name=car, production_start__year=year)
    defects = Defect.objects.filter(target=revision).all()

    return render(request, 'detail.html', dict(
        revision=revision,
        defects=defects,
    ))


def search(request):
    q = request.GET.get('q')

    cars = Car.objects.filter(name__contain=q).all()
    

    return render(request, 'search.html', dict(
        q=q,
    ))
