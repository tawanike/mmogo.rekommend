from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    cover = models.ImageField(upload_to='categories/covers/', null=True, blank=True)
    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subcategories = models.ManyToManyField("categories.Category", 
                                                related_name="sub_categories", blank=True)

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        db_table = 'categories'
        ordering = ['ordering', 'title']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'