from collections import defaultdict

from datetime import date
from django.conf import settings
from django.core.management import BaseCommand
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from desucar.models import Car, Maker,\
    OfficialDefect,\
    Community, CommunityDefect, CommunityDefectPost,\
    SuddenAccelReport, \
    NHTSADefect


def format_date(s):
    s = s.replace('-', '')
    if not s:
        return None
    if s == '발표내용 없음':
        return None
    s = s.replace('(게시일)', '')
    if s.endswith('.'):
        s = s[:-1]
    print(s)
    ys, ms, ds = s.split('.')
    y, m, d = int(ys), int(ms), int(ds)
    return date(year=y, month=m, day=d)


def parse_int(s):
    s = s.replace(',', '')
    return int(s)


def parse_report_date(s):
    if '.' in s:
        ys, ms, ds = s.split('.')
        return int(ys), int(ms), int(ds)
    else:
        return int(s), None, None


not_exists = [
    'a400', 'w300', 'w500', 'ea00', 'vd00', 'be00', 'ev00',
    'fe00', 'yi01', 'ym01', 'zp00', 'vr00', 'yr00', 'bs00',
]


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
        NHTSADefect.objects.all().delete()

        gs = gspread.authorize(cred)
        cars_doc = gs.open_by_key('1EMOGtpBJ9sW2RTZMjZ7UGQ7ODQgDjruyp-YsW5g1AgU')
        center_sheet = cars_doc.worksheet('문의처')

        contacts = {}
        for row in center_sheet.get_all_values()[1:]:
            contacts[row[0]] = row[2]

        print(contacts)

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

            maker, _ = Maker.objects.get_or_create(name=maker_name)
            maker.contact = contacts.get(row[5])
            maker.save()

            car, _ = Car.objects.get_or_create(
                maker=maker,
                name=car_name,
                simple_name=car_simple_name,
                search_keywords=search_keywords,
                code=car_code,
                make_start=make_start,
                make_end=make_end,
                n_registered=parse_int(row[2]),
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
                print(car_code)
                if car_code in not_exists:  # TODO : fix code.
                    continue

                car = Car.objects.get(code=car_code)
                if not row[10]:
                    n_targets = None
                    n_targets_comment = None
                elif row[10] in [
                    '증상 발생 차량 전체',
                    '해당차량 전체',
                    '증상 발생하는 차량 전체',
                    '조치시점까지 생산된 해당 차량 전체',
                    '스티커 미부착 차량 전체',
                ]:
                    n_targets = None
                    n_targets_comment = row[10]
                else:
                    n_targets = parse_int(row[10])
                    n_targets_comment = None

                part_name = row[11]
                print(part_name)

                OfficialDefect.objects.create(
                    car=car,
                    car_detail=row[1],
                    kind=defect_type,
                    n_targets=n_targets,
                    n_targets_comment=n_targets_comment,
                    part_name=part_name,
                    solution=row[12],
                    source_name=row[14],
                    make_start=format_date(row[5]),
                    make_end=format_date(row[6]),
                    make_date_comment=row[7],
                    fix_start=row[8],
                    fix_end=row[9],
                )

        community_doc = gs.open_by_key('1odQ14CCOmN9jlL-TnSj9W37iGf8bi_AmG_VjYsp8qNg')
        communities = []
        for row in community_doc.get_worksheet(0).get_all_values()[1:]:
            print(row)

            if row[5] in ['정보 없음', '정보없음']:
                row[5] = None
            n_members = parse_int(row[5]) if row[5] else None

            community = Community.objects.create(
                name=row[4],
                url=row[7],
                n_members=n_members,
                is_active=row[6] == '활성화',
            )
            communities.append(community)

        sheet = defects_doc.worksheet('3_비공식_결함정보(동호회/제보/인터넷등)')
        defects = {}
        for row in sheet.get_all_values()[1:]:
            car_code = row[2] + row[3] + row[4]
            if car_code in not_exists:  # TODO : fix code.
                continue

            car = Car.objects.get(code=car_code)
            key = row[8]
            part_name = row[7]

            defect = CommunityDefect.objects.create(
                # community=community,
                car=car,
                part_name=part_name,
                status=row[5],
            )

            defects[key] = defect

        print(len(defects.keys()))

        sheet = defects_doc.worksheet('3_비공식_결함정보(+상세내용)')
        for row in sheet.get_all_values()[1:]:
            key = row[0]
            posted_at = format_date(row[3]) if row[3] else None

            url = row[5].strip()
            if key not in defects:
                continue  # TODO : remove

            defect = defects[key]

            print(row[6])

            CommunityDefectPost.objects.create(
                defect=defects[key],
                url=url,
                content=row[6],
                posted_at=posted_at,
                author_name=row[4],
                join_required=row[2] == '(가입해야 읽을 수 있음)',
            )
            print(url)

            if row[1]:
                defect.editor_comment = row[1]
            community = [c for c in communities if c.url in url][0]
            defect.community = community
            defect.save()

        sheet = defects_doc.worksheet('4_급발진_의심신고(국토부/소비자원)')
        for row in sheet.get_all_values()[1:]:
            car_code = row[2] + row[3] + row[4]

            if car_code in not_exists:
                continue

            car = Car.objects.get(code=car_code)

            report_year, report_month, report_day = parse_report_date(row[9])
            SuddenAccelReport.objects.create(
                car=car,
                car_detail=row[5] + ' ' + row[6],
                accident_at=format_date(row[7]),
                detail=row[10],
                source=row[11],
                report_at_year=report_year,
                report_at_month=report_month,
                report_at_day=report_day,
            )
            print(row[10])

        sheet = defects_doc.worksheet('5_미국_리콜')
        for row in sheet.get_all_values()[1:]:
            car_code = row[2] + row[3] + row[4]
            car = Car.objects.get(code=car_code)

            NHTSADefect.objects.create(
                car=car,
                car_detail=row[1],
                recall_code=row[9],
                n_targets=parse_int(row[10]),
                make_start=format_date(row[5]),
                make_end=format_date(row[6]),
                make_date_comment=row[7],
                fix_start=format_date(row[8]),
                part_name=row[12],
                original_part_name=row[11],
                original_defect=row[14],
                original_summary=row[13],
                original_solution=row[15]
            )
            print(row)
            print(car)
