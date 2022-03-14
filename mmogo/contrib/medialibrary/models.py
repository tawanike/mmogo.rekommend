from django.db import models


class MediaLibrary(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='media-library/')
    file_type = models.CharField(max_length=100)
    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # If not enhanced queue for processing to extract features such as colour, scene etc
    is_enhanced = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'medialibrary'
        verbose_name = 'Media Library'
        verbose_name_plural = 'Media Library'
