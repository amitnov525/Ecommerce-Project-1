from django.contrib import admin
from store_app.models import Products,ProductGallry
from store_app.models import Variation,ReviewRating
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class Productgallryinline(admin.TabularInline):
    model=ProductGallry
    extra=1

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price','stock','category','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)}
    inlines=[Productgallryinline]

admin.site.register(Products,ProductAdmin)

class VariationDisplay(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_active']
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value')
admin.site.register(Variation,VariationDisplay)

admin.site.register(ReviewRating)
admin.site.register(ProductGallry)