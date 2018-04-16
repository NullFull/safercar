from django.contrib import admin
from django.urls import path
from desucar import views
from carticle import views as article_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('about', views.about),
    path('search', views.search),
    path('<maker_name>/<car_name>-<int:car_year>-<car_code>', views.detail),
    path('suggest', views.suggest),

    path('articles/', article_views.article_list),
    path('articles/<int:article_id>', article_views.article_detail),
]
