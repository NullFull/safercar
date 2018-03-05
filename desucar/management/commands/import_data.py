from datetime import date
from django.conf import settings
from django.core.management import BaseCommand
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from desucar.models import Car, Maker, OfficialDefect, CommunityDefect, Community, SuddenAccelReport


def format_date(s):
    if not s:
        return None
    s = s.replace('(게시일)', '')
    if s.endswith('.'):
        s = s[:-1]
    ys, ms, ds = s.split('.')
    y, m, d = int(ys), int(ms), int(ds)
    return date(year=y, month=m, day=d)


def parse_int(s):
    s = s.replace(',', '')
    return int(s)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cred = ServiceAccountCredentials.from_json_keyfile_dict(
            settings.GSPREAD_AUTH,
            scopes=['https://spreadsheets.google.com/feeds']
        )

        Maker.objects.all().delete()
        Car.objects.all().delete()
        OfficialDefect.objects.all().delete()
        CommunityDefect.objects.all().delete()
        Community.objects.all().delete()

        gs = gspread.authorize(cred)
        cars_doc = gs.open_by_key('1EMOGtpBJ9sW2RTZMjZ7UGQ7ODQgDjruyp-YsW5g1AgU')
        cars_sheet = cars_doc.worksheet('대상차종 구체화')

        for row in cars_sheet.get_all_values()[1:]:
            # print(row)
            maker_name = row[3]
            car_simple_name = row[4]
            car_code = row[5] + row[6] + row[7]
            car_name = row[8]
            search_keywords = row[9]
            make_start = format_date(row[10])
            make_end = None if row[11] == 'on' else format_date(row[11])

            if search_keywords:
                search_keywords = search_keywords.split(',')

            print(car_name)
            print(search_keywords)

            maker, _ = Maker.objects.get_or_create(name=maker_name)
            car, _ = Car.objects.get_or_create(
                maker=maker,
                name=car_name,
                simple_name=car_simple_name,
                code=car_code,
                make_start=make_start,
                make_end=make_end,
            )

        defects_doc = gs.open_by_key('1NC7CVJUPZzSw7_hEANafQiCvvP331p8oNWLtCi3z53Y')

        sheet_names = [
            ('1_리콜(국토교통부)', OfficialDefect.종류.리콜),
            ('1_리콜(환경부)', OfficialDefect.종류.리콜),
            ('2_무상수리(국토교통부)', OfficialDefect.종류.무상수리),
            ('2_무상수리(CISS)', OfficialDefect.종류.무상수리),
        ]

        for sheet_name, defect_type in sheet_names:
            sheet = defects_doc.worksheet(sheet_name)
            for row in sheet.get_all_values()[1:]:
                car_code = row[2] + row[3] + row[4]
                if not car_code:
                    # TODO : remove
                    # CISS 시트에 빈 아이들 많음
                    continue

                car = Car.objects.get(code=car_code)
                if row[10] in [
                    '증상 발생 차량 전체',
                    '해당차량 전체',
                    '증상 발생하는 차량 전체',
                    '조치시점까지 생산된 해당 차량 전체',
                    '스티커 미부착 차량 전체',
                ]:
                    row[10] = '0'

                part_name = row[11]
                print(part_name)

                OfficialDefect.objects.create(
                    car=car,
                    kind=defect_type,
                    n_targets=parse_int(row[10]),
                    part_name=part_name,
                    solution=row[12],
                    fix_start=format_date(row[8]),
                )

        sheet = defects_doc.worksheet('3_비공식_결함처리(동호회/제보/인터넷등)')
        for row in sheet.get_all_values()[1:]:
            car_code = row[2] + row[3] + row[4]
            if not car_code:  # TODO : remove
                continue

            car = Car.objects.get(code=car_code)

            community, _ = Community.objects.get_or_create(
                name=row[10],
                join_required=row[12] == '(가입해야 읽을 수 있음)',
                url=row[11]
            )

            CommunityDefect.objects.create(
                community=community,
                car=car,
                status=row[7],
                solution=row[14]
            )

        sources = set()

        sheet = defects_doc.worksheet('5_급발진_의심신고(국토부/소비자원)')
        for row in sheet.get_all_values()[1:]:
            car_code = row[2] + row[3] + row[4]

            car = Car.objects.get(code=car_code)

            SuddenAccelReport.objects.create(
                car=car,
                detail=row[10],
            )

            sources.add(row[11])

        print(sources)
