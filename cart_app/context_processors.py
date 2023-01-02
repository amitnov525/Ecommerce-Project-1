from cart_app.models import Cart, CartItem 
from cart_app.views import _cart

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    try:
        cart_id=Cart.objects.filter(cartid=_cart(request))
        if request.user.is_authenticated:
            cart_items=CartItem.objects.all().filter(user=request.user)
        else:
            cart_items=CartItem.objects.all().filter(cart=cart_id[:1])
        for cart_item in cart_items:
            cart_count+=cart_item.quantity
            
    except Cart.DoesNotExist:
        cart_count=0
    return {'cart_count':cart_count}

