from django.shortcuts import render
from .models import Article, Commentary
from django.views import generic


class IndexView(generic.ListView):
    model = Article
    paginate_by = 5
    queryset = Article.objects.all().order_by('-added')


class DetailView(generic.DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['comments'] = Commentary.objects.all()
        return context
