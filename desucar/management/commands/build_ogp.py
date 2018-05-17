from desucar.models import Car
from os import path
from django.conf import settings
from django.core.management import BaseCommand
from wand.drawing import Drawing
from wand.image import Image


# TODO : move to settings
OGP_BASE_PATH = path.join(settings.DATA_DIR, 'base_ogp.png')
FONT_PATH = path.join(settings.DATA_DIR, 'NotoSansCJKkr-Medium.otf')
# SOURCE_DIR = path.join(settings.DATA_DIR, 'cars')
SOURCE_DIR = path.join(settings.BASE_DIR, 'desucar', 'static', 'cars')
TARGET_DIR = path.join(settings.BASE_DIR, 'desucar', 'static', 'ogp')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(OGP_BASE_PATH)
        base_img = Image(filename=OGP_BASE_PATH)
        for car in Car.objects.all():
            ogp_filename = path.join(TARGET_DIR, car.code + '.png')
            car_filename = path.join(SOURCE_DIR, car.code + '-750x.png')

            if not path.exists(car_filename):
                print(car_filename)
                print('not exists')
                continue

            with base_img.clone() as ogp_image:
                with Drawing() as draw:
                    draw.font = FONT_PATH
                    draw.text_alignment = 'left'
                    draw.font_size = 40
                    draw.text(70, 90, car.maker.name + ' ' + car.name)
                    draw(ogp_image)

                with Image(filename=car_filename) as car_image:
                    ogp_image.composite(car_image, left=422, top=192)
                ogp_image.save(filename=ogp_filename)
