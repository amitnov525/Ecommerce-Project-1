from django.contrib import admin
from cart_app.models import Cart,CartItem

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['cartid','date_added']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['product','cart','quantity','is_active']



