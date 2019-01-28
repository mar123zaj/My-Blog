from django.shortcuts import render
from .models import Article, Commentary, Profile
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView, FormView
from django.contrib.auth.views import PasswordResetView
from article.forms import ContactForm, SignUpForm, CommentForm, ArticleForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from article.tokens import account_activation_token
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from article.tokens import account_activation_token
from django.http import Http404

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
    return render(request, 'thanks.html')


def add_article(request):
    user = request.user
    form = ArticleForm()
    if user.has_perm('article.can_add_article'):
        return render(request, 'article/article_form.html', {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = user
            article.save()
            return redirect('detail', pk=article.pk)
    else:
        return render(request, 'article/permission.html')


def add_comment(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST" and user.groups.filter(name="Users").count():
        form = CommentForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.article = article
            commentary.nick = user
            commentary.save()
            return redirect('detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'article/commentary_form.html', {'form': form})


def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    return user.is_authenticated


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    elif not is_authenticated(request.user):
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return redirect('logout')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        group = get_object_or_404(Group, name='Users')
        user.groups.add(group)
        user.is_active = True
        user.profile.email_confirmed = True
        user.groups.add(Group.objects.get(name='Users'))
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


class EditProfile(UpdateView):
    template_name = 'article/profile_edit.html'
    model = Profile
    fields = ['bio', 'country']

    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user)


class ViewProfile(generic.DetailView):
    model = Profile
    template_name = 'article/profile.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user)