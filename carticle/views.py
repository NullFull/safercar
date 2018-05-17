from collections import OrderedDict
from datetime import date
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import Http404
from django.shortcuts import render
from .models import Article


# 퍼블리싱이 django template 기반으로 되서 옮기기 귀찮아서 DB코델에서 하드코드로 옮김.
# 어차피 추가 없을거면 이게 빠를듯... 마음에 안드는 사람이 고칩니다.
carticles = OrderedDict({
    1: {
        'id': 1,
        'title': '차쓸신잡(1) 한국인이 가장 오래타는 차 베스트 10',
        'summary': '''우리나라에서 운행중인 차 10대 중 1대는 출시된 지 15년이 넘은 차입니다. 한국인들은 어떤 차를 가장 아끼며 오래 타고 있을까요? '차쓸신잡'에서 가장 많이 운행되고 있는 10대 차종을 알아봤습니다.''',
        'thumbnail': static('carticle/car/image1-1.jpg'),
        'template': 'carticle/detail/detail1.html',
        'date_published': date(2018, 3, 9),
    },
    2: {
        'id': 2,
        'title': '차쓸신잡(2) 늑장리콜 상습범을 수배합니다 (늑장리콜 국내차 10종)',
        'summary': '''차주 여러분은 제조사의 리콜 발표를 주의깊게 보고 계신가요? 어떤 차는 출시된 직후 리콜을 실시하지만, 간혹 출시 후 한참 지나 리콜을 하는 경우도 있습니다. '차쓸신잡'에서 출시와 리콜 시점의 기간이 가장 긴 '늑장리콜' 사례를 모았습니다.''',
        'thumbnail': static('carticle/car/image2-3.jpg'),
        'template': 'carticle/detail/detail2.html',
        'date_published': date(2018, 3, 9),
    },
    3: {
        'id': 3,
        'title': '차쓸신잡(3) 국내에서 가장 많은 사람들이 타는 100대 차종은?',
        'summary': '''2017년말 기준으로 공식 등록된 차는 약 2천2백만 대. 우리나라 인구 두 명 가운데 한 명은 차를 가지고 있는 셈입니다. 그렇다면 가장 많은 사람이 타는 차는 무엇일까요? '차쓸신잡'에서 판매량이 많은 차종 100대를 찾아봤습니다.''',
        'thumbnail': static('carticle/car/image3-1.png'),
        'template': 'carticle/detail/detail3.html',
        'date_published': date(2018, 3, 9),
    },
    4: {
        'id': 4,
        'title': '차쓸신잡(4) 국내 100대 차종의 동호회 리스트를 공개합니다',
        'summary': '''차를 긴 시간 타고 다니면서 이런저런 경험을 해본 사람만 알게 되는 '꿀팁'이 있기 마련입니다. 이런 정보들은 보통 '자동차 동호회'에 모이기 마련이죠. '차쓸신잡'에서 우리나라 100대 차종의 동호회 리스트를 모아봤습니다.''',
        'thumbnail': static('carticle/car/image4-1.png'),
        'template': 'carticle/detail/detail4.html',
        'date_published': date(2018, 3, 9),
    },
    5: {
        'id': 5,
        'title': '차쓸신잡(5) 급발진 1탄 : 급발진 의심사고가 가장 많았던 차는?',
        'summary': '''급발진 의심 사고가 가장 많은 차종은 무엇일까요? '차쓸신잡'에서 2000년부터 18년 동안 정부에 신고된 급발진 의심 사고 신고내역 1천여 건을 분석했습니다. 먼저 가장 신고건수가 많은 3대 차종과 10만대당 신고건수가 많은 제작사 3곳입니다.''',
        'thumbnail': static('carticle/car/image5-1.png'),
        'template': 'carticle/detail/detail5.html',
        'date_published': date(2018, 3, 9),
    },
    6: {
        'id': 6,
        'title': '차쓸신잡(6) 급발진 2탄 : 주차장 세차장 미스터리',
        'summary': '''2017년 한 해에만 신고된 급발진 의심사고가 73건. 제작사는 운전자의 실수가 원인이라고 주장하지만, 그렇다고 보기 어려운 경우도 적지 않습니다. 이번 '차쓸신잡'에서는 엑셀을 잘못 밟았더라도 급발진으로 이어지기는 어려운 사례들을 정리했습니다.''',
        'thumbnail': static('carticle/car/image6-1.png'),
        'template': 'carticle/detail/detail6.html',
        'date_published': date(2018, 3, 9),
    }
})


def article_list(request):
    return render(request, 'carticle/list.html', dict(
        articles=carticles.items()
    ))


def article_detail(request, article_id):
    if article_id not in carticles:
        raise Http404

    article = carticles.get(article_id)

    return render(request, article['template'], dict(
        title=article['title'],
    ))
