from django.db import models

class Brand(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='brands/', blank=True, null=True)
    cover = models.ImageField(
        upload_to='brands/covers/', blank=True, null=True)

    class Meta:
        db_table = 'brands'
        ordering = ['title']
        verbose_name = 'Brand'
        verbose_name_plural = "Brands"

    def __str__(self) -> str:
        return str(self.title)
