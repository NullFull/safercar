from django.contrib.admin import site
from desucar.models import Maker, Car, Revision, Defect

site.register([Maker, Car, Revision, Defect])
