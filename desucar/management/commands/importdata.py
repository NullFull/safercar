from datetime import date
from django.conf import settings
from django.core.management import BaseCommand
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from desucar.models import Car, Maker, Defect


def format_date(s):
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
        Defect.objects.all().delete()

        gs = gspread.authorize(cred)
        cars_doc = gs.open_by_key('1EMOGtpBJ9sW2RTZMjZ7UGQ7ODQgDjruyp-YsW5g1AgU')
        cars_sheet = cars_doc.worksheet('대상차종 구체화')

        for row in cars_sheet.get_all_values()[1:]:
            maker_name = row[3]
            car_simple_name = row[4]
            car_code = row[5] + row[6] + row[7]
            car_name = row[8]
            make_start = format_date(row[9])
            make_end = None if row[10] == 'on' else format_date(row[10])

            print(car_name)

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
            '1_리콜(국토교통부)',
            '1_리콜(환경부)',
            '2_무상수리(국토교통부)',
            '2_무상수리(CISS)',
        ]

        for sheet_name in sheet_names:
            sheet = defects_doc.worksheet(sheet_name)
            for row in sheet.get_all_values()[1:]:
                car_code = row[2] + row[3] + row[4]
                car = Car.objects.get(code=car_code)
                if row[10] in [
                    '증상 발생 차량 전체',
                    '해당차량 전체',
                    '증상 발생하는 차량 전체',
                    '조치시점까지 생산된 해당 차량 전체',
                    '스티커 미부착 차량 전체',
                ]:
                    row[10] = '0'

                print(row[11])
                Defect.objects.create(
                    car=car,
                    kind=Defect.종류.무상수리,
                    n_targets=parse_int(row[10]),
                    part_name=row[11],
                    solution=row[12],
                    fix_start=format_date(row[8]),
                )
