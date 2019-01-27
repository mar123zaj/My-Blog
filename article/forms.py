from django import forms
from django.core.mail import send_mail
from .models import Commentary



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


class CommentForm(forms.ModelForm):

    class Meta:
        model = Commentary
        fields = ('nick', 'title', 'comment', )


