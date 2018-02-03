from django.contrib.admin import site
from desucar.models import Maker, Car, Defect

site.register([Maker, Car, Defect])
