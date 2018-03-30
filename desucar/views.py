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
            'desc': '리콜은 소비자의 안전을 위협하는 중대한 결함을 바로잡기 위해 시행합니다. 이곳에서는 <a href="www.car.go.kr">국토교통부 자동차리콜센터</a>와 환경부가 제공한 2000년 이후 리콜 자료 전체를 보여드립니다.',
            'last_update': date(2018, 3, 31),
            'items': [x for x in official_defects if x.kind == 'RC'],
        },
        '무상수리': {
            'code': 'freefix',
            'desc': '무상수리는 리콜 대상이 아닌 다양한 제작 결함을 바로잡기 위해 시행합니다. 이곳에서는 <a href="www.car.go.kr">국토교통부 자동차리콜센터</a>와 <a href="www.ciss.go.kr">한국소비자원 소비자위해감시시스템</a>에 등록된 2000년 이후 무상수리 자료 전체를 보여드립니다.',
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
        cars=query.order_by('-id').all(),
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
