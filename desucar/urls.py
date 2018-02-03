from django.contrib import admin
from django.urls import path
from desucar import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('search', views.search),
    path('<maker_name>/<car_name>-<int:car_year>-<car_code>', views.detail),

    # path('<maker>/<car>/<int:year>', views.detail),
]
