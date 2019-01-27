from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    title = models.CharField(max_length=150)
    added = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    picture = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Commentary(models.Model):
    nick = models.CharField(max_length=20)
    title = models.CharField(max_length=15)
    comment = models.TextField(max_length=300)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


