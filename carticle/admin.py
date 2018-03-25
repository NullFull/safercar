from django.contrib.admin import site
from carticle.models import Article

site.register([Article, ])
