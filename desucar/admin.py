from django.contrib.admin import site
from desucar.models import Maker, Car, OfficialDefect, CommunityDefect, SuddenAccelReport, NHTSADefect

site.register([Maker, Car, OfficialDefect, CommunityDefect, SuddenAccelReport, NHTSADefect])
