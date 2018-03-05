from django.contrib.admin import site
from desucar.models import Maker, Car, OfficialDefect

site.register([Maker, Car, OfficialDefect])
