from django.contrib import admin
from .models import Product, ProductVariation, Bundle


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', 'category__title', 'brand__title',)
    list_display = ('title', 'category__title', 'price',
                    'featured', 'published', )
    list_filter = ('featured', 'published',)
    readonly_fields = ('tags',)
    prepopulated_fields = {'slug' : ('title',),}


class ProductVariationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',),}

class BundleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',),}

# class ProductLocationAdmin(admin.ModelAdmin):
#     search_fields = ('id', 'product', 'location', 'supplier', 'reorder_level', 'product_name',)
#     list_display = ('product_name', 'location_id', 'supplier_id', 'reorder_level','created_at',)


admin.site.register(Bundle, BundleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
# admin.site.register(ProductLocation, ProductLocationAdmin)
