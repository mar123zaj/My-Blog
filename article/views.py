from django.shortcuts import render
from .models import Article, Commentary
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.core.mail import send_mail
from article.forms import ContactForm
from django.views.generic.edit import FormView


class IndexView(generic.ListView):
    model = Article
    paginate_by = 8
    queryset = Article.objects.all().order_by('-added')


class DetailView(generic.DetailView):
    model = Article


class OutUser(LogoutView):
    next_page = '/'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
