from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import datetime


class Category(models.Model):  # blogpost, service, product
    name = models.TextField(blank=False)
    created = models.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.TextField(null=False, unique=True)
    description = models.TextField()
    primary_image = models.TextField()
    secondary_images = ArrayField(
        models.TextField(
            help_text='optional images to show if needed'),
        null=True
    )
    hero_post = models.BooleanField(
        default=False,
        help_text='Is it to be placed on top of the service page? default to false'
    )
    author = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        null=True
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.CASCADE,
        null=True
    )
    created = models.DateTimeField(default=datetime.datetime.utcnow)
    updated = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Product(Post):
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    email = models.TextField(blank=False)
    comment = models.TextField()
    blogpost = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(default=datetime.datetime.utcnow)

