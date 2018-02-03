import csv

from django.conf import settings
from django.core.management import BaseCommand
from os import path

from desucar.models import Car, Maker


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Maker.objects.all().delete()
        Car.objects.all().delete()

        data_dir = path.join(settings.BASE_DIR, 'data')
        csv_path = path.join(data_dir, 'cars.csv')

        with open(csv_path) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                maker_name = row[3]
                print(maker_name)
                car_name = row[8]
                print(car_name)

                maker, _ = Maker.objects.get_or_create(name=maker_name)
                car, _ = Car.objects.get_or_create(maker=maker, name=car_name)
