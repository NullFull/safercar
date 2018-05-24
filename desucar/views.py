import json
from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.cache import cache_page

from desucar.models import Car, Maker
from desucar.utils.search import Searcher


@cache_page(30)
def index(request):
    return render(request, 'index.html', dict(
        makers=Maker.objects.all(),
        cars=Car.objects.all(),
    ))


@cache_page(30)
def detail(request, maker_name, car_name, car_year, car_code):
    car = Car.objects.get(code=car_code)
    official_defects = car.official_defects.all()
    defects = {
        '리콜': {
            'code': 'recall',
            'desc': '리콜은 소비자의 안전을 위협하는 중대한 결함을 바로잡기 위해 시행합니다. 이곳에서는 <a href="http://www.car.go.kr">국토교통부 자동차리콜센터</a>와 환경부가 제공한 2000년 이후 리콜 자료 전체를 보여드립니다.',
            'last_update': date(2018, 3, 31),
            'items': [x for x in official_defects if x.kind == 'RC'],
        },
        '무상수리': {
            'code': 'freefix',
            'desc': '무상수리는 리콜 대상이 아닌 다양한 제작 결함을 바로잡기 위해 시행합니다. 이곳에서는 <a href="http://www.car.go.kr">국토교통부 자동차리콜센터</a>와 <a href="http://www.ciss.go.kr">한국소비자원 소비자위해감시시스템</a>에 등록된 2000년 이후 무상수리 자료 전체를 보여드립니다.',
            'last_update': date(2018, 3, 31),
            'items': [x for x in official_defects if x.kind == 'FF'],
        },
        '비공식 결함': {
            'code': 'unofficial',
            'desc': '공식적으로 알려진 리콜이나 무상수리 외에도 비공식적으로 처리되는 중요한 결함 정보들이 많습니다. 이곳에서는 자동차 관련 커뮤니티에서 수집된 다양한 비공식 결함 정보를 알려드립니다.',
            'last_update': date(2018, 3, 31),
            'items': list(car.community_defects.all()),
        },
        '급발진 의심': {
            'code': 'sudden-accel',
            'desc': '2000년 이후 국토교통부와 한국소비자원에 신고된 급발진 의심 사고는 800여건이 넘지만, 지금까지 제작사나 정부가 인정한 급발진 사고는 0건입니다. 이곳에서는 차종별로 신고된 급발진 의심 사고의 구체적인 내용을 알려드립니다.',
            'last_update': date(2018, 3, 31),
            'items': list(car.sudden_accels.all()),
        },
        '미국 리콜': {
            'code': 'nhtsa',
            'desc': '2000년 이후 미국 내 자동차 리콜 1만3천여건을 분석해 국내에서 판매 중인 차종의 결함 정보를 알려드립니다. 단, 일부 차종의 경우 국내외 판매 사양에 차이가 있어 미국 리콜 데이터가 국내에 적용되지 않을 수 있습니다.',
            'last_update': date(2018, 5, 25),
            'items': list(car.nhtsa_defects.all()),
        }
    }

    for key, defect in defects.items():
        defects[key]['count'] = len(defects[key]['items'])

    return render(request, 'detail.html', dict(
        car=car,
        official_defects=official_defects,
        defects=defects,
    ))


@cache_page(30)
def search(request):
    q = request.GET.get('q').strip()

    data = json.load(open(settings.SEARCH_MAP_PATH))
    searcher = Searcher(data['makers'], data['cars'])

    makers, cars, year = searcher.search(q)

    return render(request, 'search.html', dict(
        q=q,
        cars=cars,
    ))


@cache_page(30)
def suggest(request):
    q = request.GET.get('q').strip()

    data = json.load(open(settings.SEARCH_MAP_PATH))
    searcher = Searcher(data['makers'], data['cars'])

    makers, cars, year = searcher.search(q)

    return HttpResponse(serializers.serialize('json', cars), content_type='application/json')


@cache_page(30)
def about(request):
    return render(request, 'about.html')
