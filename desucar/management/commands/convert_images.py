from os.path import splitext

from django.conf import settings
from django.core.management import BaseCommand
from os import path, listdir, makedirs
from wand.image import Image


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        SRC_DIR = path.join(settings.BASE_DIR, 'data', 'cars')
        TARGET_DIR = path.join(settings.BASE_DIR, 'desucar', 'static', 'cars')
        makedirs(TARGET_DIR, exist_ok=True)

        for filename in listdir(SRC_DIR):
            if filename == '.DS_Store':
                continue

            basename, ext = splitext(filename)
            src_img_path = path.join(SRC_DIR, filename)

            print(basename)

            with Image(filename=src_img_path) as img:
                detail_img_path = path.join(TARGET_DIR, basename + '-600x.png')
                detail_img = img.clone()
                detail_img.transform(resize='600x')
                detail_img.save(filename=detail_img_path)

                ogp_img_path = path.join(TARGET_DIR, basename + '-750x.png')
                ogp_img = img.clone()
                ogp_img.transform(resize='750x')
                ogp_img.save(filename=ogp_img_path)

                list_img_path = path.join(TARGET_DIR, basename + '-200x.png')
                list_img = img.clone()
                list_img.transform(resize='200x')
                list_img.save(filename=list_img_path)
