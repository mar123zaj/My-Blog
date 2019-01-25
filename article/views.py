from django.shortcuts import render
from .models import Article, Commentary
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView


class IndexView(generic.ListView):
    model = Article
    paginate_by = 8
    queryset = Article.objects.all().order_by('-added')


class DetailView(generic.DetailView):
    model = Article


class OutUser(LogoutView):
    next_page = '/'


