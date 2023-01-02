from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,first_name,last_name,email,username,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
            )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save()
        return user



class MyUser(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=254,unique=True)
    phone_number=models.CharField(max_length=50)

    last_login=models.DateTimeField(auto_now_add=True)
    data_joined=models.DateField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    objects=MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(blank=True,max_length=50)
    profile_picture=models.ImageField(blank=True,upload_to='userprofile')
    city=models.CharField(blank=True,max_length=50)
    state=models.CharField(blank=True,max_length=50)
    country=models.CharField(blank=True,max_length=50)
    zipcode=models.CharField(blank=True,max_length=50)

    def __str__(self):
        return self.user.first_name
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'