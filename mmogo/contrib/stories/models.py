from django.db import models
from mmogo.contrib.categories.models import Category

class Story(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)
    image = models.ImageField(upload_to='stories', blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name="story_category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.title)
    
    class Meta:
        db_table = 'stories'
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
