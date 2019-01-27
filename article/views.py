from django.shortcuts import render
from .models import Article, Commentary
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView, FormView
from django.contrib.auth.views import PasswordResetView
from article.forms import ContactForm, FormSignUp
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from article.forms import FormSignUp
from article.tokens import account_activation_token
from django.shortcuts import get_object_or_404, redirect


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


class CreateArticle(CreateView):
    model = Article
    fields = ['title', 'text', 'picture']


class CreateComment(CreateView):
    model = Commentary
    fields = ['title', 'text', 'picture']



def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.article = article
            commentary.save()
            return redirect('detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'article/commentary_form.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = FormSignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = FormSignUp()
    return render(request, 'registration/signup.html', {'form': form})
