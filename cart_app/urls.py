from django.urls import path 
from cart_app import views

urlpatterns=[
    path('',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('minus_cart/<int:product_id>/<int:cart_item_id>/',views.minus_cart,name='minus_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('checkout/',views.checkout,name='checkout'),
]