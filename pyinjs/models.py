from djongo import models
from django.utils import timezone
from mongoengine import *


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.TextField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    published_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Topic(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.text





