from django import forms
from django.core.mail import send_mail
from .models import Commentary, Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        send_mail(
            'Contact Us',
            self.cleaned_data['message'],
            '',
            ['alacris.1995@gmail.com']
        )


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text', 'picture', )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Commentary
        fields = ('nick', 'title', 'comment', )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

