from http.client import HTTPResponse
from django.shortcuts import render,redirect,get_object_or_404
from store_app.models import Products, Variation
from cart_app.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store_app.models import Variation
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request,product_id):
    product=Products.objects.get(id=product_id)
    current_user=request.user
    if request.user.is_authenticated:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key=item
                value=request.POST[key]
                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
            is_cart_item=CartItem.objects.filter(product=product,user=request.user).exists()
            if is_cart_item:
                cart_item=CartItem.objects.filter(product=product,user=request.user)
                exist_varition_list=[]
                id=[]
                for item in cart_item:
                    exist_varition=item.variation.all()
                    exist_varition_list.append(list(exist_varition))
                    id.append(item.id)
                if product_variation in exist_varition_list:
                    indx=exist_varition_list.index(product_variation)
                    product_id=id[indx]
                    item=CartItem.objects.get(product=product,id=product_id)
                    item.quantity+=1
                    item.save()
                else:
                    item=CartItem.objects.create(product=product,quantity=1,user=request.user)
                    if len(product_variation)>0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                    item.save()
            else:
                cart_item=CartItem.objects.create(
                    user=request.user,
                    quantity=1,
                    product=product
                )
                if len(product_variation)>0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                cart_item.save()
            return redirect('cart')
    else:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key=item
                value=request.POST[key]
                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart_id1=_cart(request)
            cart=Cart.objects.get(cartid=cart_id1)
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cartid=_cart(request)
            )
        cart.save()
        is_cart_item=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item:
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            exist_varition_list=[]
            id=[]
            for item in cart_item:
                exist_varition=item.variation.all()
                exist_varition_list.append(list(exist_varition))
                id.append(item.id)
            if product_variation in exist_varition_list:
                indx=exist_varition_list.index(product_variation)
                product_id=id[indx]
                item=CartItem.objects.get(product=product,id=product_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item=CartItem.objects.create(
                cart=cart,
                quantity=1,
                product=product
            )
            if len(product_variation)>0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')

def minus_cart(request,product_id,cart_item_id):
    product=get_object_or_404(Products,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Cart.objects.get(cartid=_cart(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    product=get_object_or_404(Products,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart=Cart.objects.get(cartid=_cart(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    



def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cartid1=_cart(request)
            cart=Cart.objects.get(cartid=cartid1)
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'cart_app/cart.html',context)

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        cartid1=_cart(request)
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cartid1=_cart(request)
            cart=Cart.objects.get(cartid=cartid1)
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'store_app/checkout.html',context)
