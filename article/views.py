from django.shortcuts import render
from .models import Article, Commentary
from django.views import generic


class IndexView(generic.ListView):

    def get_queryset(self):
        return Article.objects.all()
