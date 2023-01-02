from django.contrib import admin
from accounts.models import MyUser,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.

class MyAdmin(UserAdmin):
    list_display=['id','email','username','first_name','last_name','data_joined','last_login','is_active']
    readonly_fields=('data_joined','last_login')
    ordering=('-data_joined',)
    fieldsets=()
    list_filter=()
    filter_horizontal=()
admin.site.register(MyUser,MyAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    def thumnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    list_display=['thumnail','user','city','country']

admin.site.register(UserProfile,UserProfileAdmin)


