from django import forms
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        send_mail(
            'Contact Us',
            self.cleaned_data['message'],
            'me',
            ['marcin_1995@tlen.pl']
        )
