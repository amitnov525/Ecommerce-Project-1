from django.urls import path 
from store_app import views

urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_deatil'),
    path('search',views.search1,name='search'),
    path('review_rating/<int:product_id>/',views.review_rating,name='review_rating')
]
