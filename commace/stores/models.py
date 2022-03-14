from django.db import models
from django.contrib.auth.models import User

from mmogo.contrib.links.models import Link

class Store(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='shops/', blank=True, null=True)
    cover = models.ImageField(
        upload_to='shops/covers/', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="owner")
    links = models.ForeignKey(Link, blank=True, null=True, on_delete=models.CASCADE, related_name="links")


    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'shops'
        ordering = ['ordering', 'title']
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
