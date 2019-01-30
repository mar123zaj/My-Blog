from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    title = models.CharField(max_length=150)
    added = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, default='')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Commentary(models.Model):
    nick = models.ForeignKey('Profile', on_delete=models.CASCADE, max_length=20)
    comment = models.TextField(max_length=300)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.comment


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    country = models.CharField(max_length=30, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
