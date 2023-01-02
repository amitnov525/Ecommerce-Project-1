from django.urls import path 
from accounts import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password',views.reset_password,name='reset_password'),
    path('change_password',views.change_password,name='change_password'),
    path('my-order',views.myorders,name='my-order'),
    path('edit-profile',views.edit_profile,name='edit-profile'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('createprofile/<int:id>/',views.createprofile,name='createprofile')
]
