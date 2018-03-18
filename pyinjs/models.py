from djongo import models
from django.utils import timezone
from mongoengine import *
# from PyInjection.settings import DBNAME
from django.conf import settings

# connect(DBNAME)


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


# class Entry(models.Model):
#     blog = models.EmbeddedModelField(
#         model_container=Post,
#     )
#     headline = models.CharField(max_length=255)
#
#     objects = models.DjongoManager()


class EntryPost(Post):
    # post = models.EmbeddedModelField(model_container=Post,)
    pass



