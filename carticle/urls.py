from django.conf.urls import path
from . import views


urlpatterns = [
    path('', views.article_list),
    path('<int:article_id>', views.article_detail),
]
