from django.db import models

from commace.contrib.brands.models import Brand
from mmogo.contrib.medialibrary.models import MediaLibrary
from commace.stores.models import Store
from mmogo.contrib.categories.models import Category


class ProductVariation(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='products', blank=True, null=True)
    cover = models.ImageField(
        upload_to='products/covers', blank=True, null=True)

    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    promo_price = models.DecimalField(
        default=0, decimal_places=2, max_digits=12)

    sku = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    size = models.CharField(max_length=100, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)
    width = models.CharField(max_length=100, blank=True, null=True)
    pack_size = models.CharField(max_length=100, blank=True, null=True)
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=12)
    margin = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    dispenser_barcode = models.CharField(max_length=100, blank=True, null=True)
    outercase_barcode = models.CharField(max_length=100, blank=True, null=True)
    pallet_barcode = models.CharField(max_length=100, blank=True, null=True)

    reorder_level = models.IntegerField(
        default=0, blank=True, null=True)
    reorder_quantity = models.IntegerField(
        default=5, blank=True, null=True)
    quantity = models.IntegerField(
        default=0, blank=True, null=True)

    def __str__(self):
        return str(self.title)
        
    class Meta:
        db_table = 'product_variations'
        verbose_name = 'Product Variation'
        verbose_name_plural = 'Product Variations'


class Product(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='products', blank=True, null=True)
    cover = models.ImageField(
        upload_to='products/covers', blank=True, null=True)
    images = models.ManyToManyField(MediaLibrary, related_name='product_media', blank=True, null=True)

    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    promo_price = models.DecimalField(
        default=0, decimal_places=2, max_digits=12)

    category = models.ForeignKey(
        Category, related_name="product_category", on_delete=models.CASCADE)
    brand = models.ForeignKey(
        Brand, related_name="product_brand", on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Store, related_name="product_shop", on_delete=models.CASCADE, blank=True, null=True)

    sku = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    variations = models.ManyToManyField(
        ProductVariation, related_name="variations", blank=True)

    tags = models.JSONField(default=None, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)
    width = models.CharField(max_length=100, blank=True, null=True)
    pack_size = models.CharField(max_length=100, blank=True, null=True)
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=12)
    margin = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    dispenser_barcode = models.CharField(max_length=100, blank=True, null=True)
    outercase_barcode = models.CharField(max_length=100, blank=True, null=True)
    pallet_barcode = models.CharField(max_length=100, blank=True, null=True)

    reorder_level = models.IntegerField(
        default=0, blank=True, null=True)
    reorder_quantity = models.IntegerField(
        default=5, blank=True, null=True)
    quantity = models.IntegerField(
        default=0, blank=True, null=True)
    # supplier = models.ForeignKey(
    #     to=CompanySupplier, on_delete=models.CASCADE, blank=True, null=True)  # Deprecated

    def __str__(self):
        return str(self.title)

    @property
    def category__title(self):
        return str(self.category.title)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Bundle(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='bundles', blank=True, null=True)
    cover = models.ImageField(
        upload_to='bundles/covers', blank=True, null=True)
    images = models.ManyToManyField(MediaLibrary, related_name='bundle_media', blank=True, null=True)

    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    promo_price = models.DecimalField(
        default=0, decimal_places=2, max_digits=12)

    category = models.ForeignKey(
        Category, related_name="bundle_category", on_delete=models.CASCADE)

    brand = models.ForeignKey(
        Brand, related_name="bundle_brand", on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Store, related_name="bundle_shop", on_delete=models.CASCADE, blank=True, null=True)

    sku = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    code = models.CharField(max_length=255, blank=True, null=True)
    
    products = models.ManyToManyField(Product, related_name='product_bundles')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Bundle'
        verbose_name_plural = 'Bundles'



# class ProductLocation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     location = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     supplier = models.ForeignKey(CompanySupplier, on_delete=models.CASCADE)
#     reorder_level = models.IntegerField(default=0)
#     reorder_quantity = models.IntegerField(default=5)
#     quantity = models.IntegerField(default=0)
#     cost = models.FloatField(default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return str(self.product)

#     @property
#     def product_name(self):
#         return str(self.product.title)

#     class Meta:
#         db_table = 'product_locations'
#         verbose_name = 'Product Location'
#         verbose_name_plural = 'Product Locations'
