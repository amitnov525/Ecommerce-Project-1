from django.shortcuts import render,redirect
from cart_app.models import CartItem
from order_app.forms import OrderForm
from order_app.models import Order,Payment,OrderProduct
import datetime
import json
from store_app.models import Products
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def payments(request):
    body=json.loads(request.body)
    user=request.user 
    order_number=body['orderID']
    order=Order.objects.get(user=user,is_ordered=False,order_number=order_number)
    payment=Payment(
                    user=user,
                    payment_id=body['transID'],
                    payment_method=body['payment_method'],
                    amount_paid=order.order_total,
                    status=body['status']
    )
    payment.save()
    order.payment=payment
    order.is_ordered=True 
    order.save()
    # moving all products form cart to order product.\
    cart_items=CartItem.objects.filter(user=user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.user_id=user.id
        orderproduct.payment=payment
        orderproduct.product_id=item.product.id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()
        cart_item=CartItem.objects.get(id=item.id)
        product_variations=cart_item.variation.all()
        orderproduct=OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variations)
        orderproduct.save()
        #reducing the product stock
        product=Products.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()
    cart_items.delete()

    #sending Mail to User.
    mail_subject="Ordered Received"
    message=render_to_string('order_app/orederreceived.html', {
        'user':request.user,
        'order':order
        })
    to_email=request.user.email 
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    # send response to function sendData.
    data={
        'order':order.order_number,
        'transactionID':payment.payment_id,
    }
    return JsonResponse(data)

@login_required(login_url='login')
def place_order(request,total=0,quantity=0):
    user=request.user
    cart_item=CartItem.objects.filter(user=user)
    cart_count=cart_item.count()
    if cart_count<=0:
        return redirect('store')
    grand_total=0
    tax=0
    for item in cart_item:
        total+=(item.product.price*item.quantity)
        quantity+=item.quantity
    tax=(2*total)/100
    grand_total=total+tax 
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.pincode=form.cleaned_data['pincode']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax 
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()
            orders=Order.objects.get(user=user,is_ordered=False,order_number=order_number)
            context={
                'order':orders,
                'cart_items':cart_item,
                'tax':tax,
                'total':total,
                'grand_total':grand_total
            }
            return render(request,'order_app/payments.html',context)
        else:
            return redirect('checkout')
    else:
        return redirect('checkout')

@login_required(login_url='login')
def Order_Complete(request):
    order_number=request.GET.get('order_number')
    transactionID=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_products=OrderProduct.objects.filter(order_id=order.id)
        subtotal=0
        for item in order_products:
            subtotal+=item.quantity*item.product_price
        
        payment=Payment.objects.get(payment_id=transactionID)
        context={
            'order':order,
            'order_products':order_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request,'order_app/order_complete.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')










