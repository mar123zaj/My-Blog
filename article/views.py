from .models import Article, Commentary, Profile
from django.views import generic
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from article.forms import ContactForm, SignUpForm, CommentForm, ArticleForm, ProfileForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from article.tokens import account_activation_token
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse


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
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = user.profile
            article.save()
            return redirect('detail', pk=article.pk)
    elif user.groups.filter(name="Authors").count():
        return render(request, 'article/article_form.html', {'form': form})
    else:
        return render(request, 'article/permission.html')


def add_comment(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST" and (user.groups.filter(name="Users").count() or user.groups.filter(name="Authors").count()):
        form = CommentForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.article = article
            commentary.nick = user.profile
            commentary.save()
            return redirect('detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'article/commentary_form.html', {'form': form})


def edit_comment(request, pk):
    user = request.user
    comment = get_object_or_404(Commentary, pk=pk)
    form = CommentForm(instance=comment)
    if request.method == 'POST' and user == comment.nick.user:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'article/edit_comment.html',
                  {'form': form, 'user': user, 'comment': comment})


def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    return user.is_authenticated


def signup(request):
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
        form = SignUpForm()
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


class EditProfile(generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "article/profile_edit.html"
    success_url = '/'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse("index")


def view_profile(request, pk):
    profile = request.user.profile
    return render(request, 'article/profile.html', {'profile': profile})


def delete_comment(request, pk):
    comment = get_object_or_404(Commentary, pk=pk)
    comment.delete()
    return redirect('index')


def about(request):
    return render(request, 'about.html')
