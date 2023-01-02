from django.urls import path
from order_app import views


urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('order-complete',views.Order_Complete,name='order_complete')
]
