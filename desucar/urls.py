from django.contrib import admin
from django.urls import path
from desucar import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('<maker>/<car>/<int:year>', views.detail),
]
