from django.shortcuts import render
from .models import Article, Commentary
from django.views import generic


class IndexView(generic.ListView):
    model = Article
    paginate_by = 5
    queryset = Article.objects.all().order_by('-added')




