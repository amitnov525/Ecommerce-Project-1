from django.db import models
from store_app.models import Products,Variation
from accounts.models import MyUser

# Create your models here.

class Cart(models.Model):
    cartid=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cartid

class CartItem(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    variation=models.ManyToManyField(Variation,blank=True)
    is_active=models.BooleanField(default=True) 

    def sub_total(self):
        return self.product.price*self.quantity

    def __str__(self):
        return str(self.product)
    


