from django.shortcuts import render
from .models import Article


def article_list(request):
    return render(request, 'carticle/list.html', dict(
        articles=Article.objects.all(),
    ))


def article_detail(request, article_id):
    return render(request, 'carticle/detail.html', dict(
        article=Article.objects.get(id=article_id)
    ))
