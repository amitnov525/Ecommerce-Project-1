from django.urls import path 
from shoping_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact-form',views.contact,name='contact')
]
