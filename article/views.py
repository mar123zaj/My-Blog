from django.shortcuts import render
from .models import Article
from django.views import generic
from django.contrib.auth.views import LogoutView, FormView
from django.contrib.auth.views import PasswordResetView
from article.forms import ContactForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm

class IndexView(generic.ListView):
    model = Article
    paginate_by = 8
    queryset = Article.objects.all().order_by('-added')


class DetailView(generic.DetailView):
    model = Article


class OutUser(LogoutView):
    next_page = '/'


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    success_url = '/accounts/password_reset/done/'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


def thanks(request):
    return render(request, template_name='thanks.html')
