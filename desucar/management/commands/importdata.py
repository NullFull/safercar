import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.http import urlquote

from desucar.models import Maker, Car, Revision, Defect


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        csv_dir = os.path.join(settings.BASE_DIR, 'csv')
        csv_path = os.path.join(csv_dir, 'molit-recalls.csv')

        Maker.objects.all().delete()
        Car.objects.all().delete()
        Revision.objects.all().delete()
        Defect.objects.all().delete()

        with open(csv_path) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                print(row)
                maker_name = row[0]
                car_names = row[1]
                if not row[5] or not row[6]:
                    continue

                ps_year, ps_month, ps_day = [int(c) for c in row[5].split('.')]  # TODO : 어디 한번 수정해보시지.
                production_start = datetime(year=ps_year, month=ps_month, day=ps_day)
                pe_year, pe_month, pe_day = [int(c) for c in row[6].split('.')]
                production_end = datetime(year=pe_year, month=pe_month, day=pe_day)

                maker, _ = Maker.objects.get_or_create(name=maker_name)
                maker.slug = urlquote(maker_name)
                maker.save()

                for car_name in car_names.split(','):
                    car, _ = Car.objects.get_or_create(maker=maker, name=car_name)
                    car.slug = urlquote(car_names)
                    car.save()

                    revision, _ = Revision.objects.get_or_create(
                        car=car,
                        production_start=production_start,
                        production_end=production_end
                    )

                    part_name = row[10]
                    n_targets = row[9]
                    if not part_name:
                        continue
                    print(part_name)
                    defect, _ = Defect.objects.get_or_create(
                        target=revision,
                        part_name=part_name,
                        n_targets=int(n_targets.replace(',', ''))
                    )
                    defect.solution = row[11]
                    defect.save()