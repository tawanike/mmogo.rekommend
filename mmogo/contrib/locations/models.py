from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=255)
    currency = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='locations/countries/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Province(models.Model):

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    country = models.ForeignKey(
        Country, related_name="country_provinces", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='locations/provinces/', blank=True, null=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'provinces'
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'


class City(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    province = models.ForeignKey(
        Province, related_name="province_cities", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='locations/cities/', blank=True, null=True)
    # Add timezone

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
