from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150)
    added = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.TextField()
    picture = models.CharField(max_length=100)

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
