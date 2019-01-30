from django import forms
from django.core.mail import send_mail
from .models import Commentary, Article, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView


class ContactForm(forms.Form):
    your_mail = forms.EmailField(max_length=254)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        send_mail(
            'Contact Us',
            self.cleaned_data['message'] + '\n\n\nContact mail: ' + self.cleaned_data['your_mail'],
            '',
            ['myblog.testmail.django@gmail.com']
        )


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Commentary
        fields = ('comment', )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'country')

    def save(self, user=None):
        user_profile = super(ProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile
