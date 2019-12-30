from django.db import models
from django.contrib.auth.models import User
import datetime


class Service(models.Model):
    title = models.TextField(null=False, unique=True)
    description = models.TextField(help_text='service description')
    service_primary_image = models.TextField(
        help_text='main image to show in layout UI')
    service_secondary_images = models.TextField(
        help_text='optional images to show if needed')
    hero_service = models.BooleanField(
        default=False, help_text='is it to be placed on top of the service page? default to false')
    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.TextField(null=False, unique=True)
    description = models.TextField()
    product_primary_image = models.TextField()
    product_secondary_images = models.TextField()
    hero_product = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.TextField(null=False, unique=True)
    description = models.TextField()
    post_primary_image = models.TextField()
    hero_post = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=datetime.datetime.utcnow)
    updated = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    email = models.TextField(blank=False)
    comment = models.TextField()
    blogpost = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(default=datetime.datetime.utcnow)
