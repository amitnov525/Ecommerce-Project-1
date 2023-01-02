from django.shortcuts import render,get_object_or_404,redirect
from category.models import Category
from store_app.models import Products,ReviewRating,ProductGallry
from cart_app.models import CartItem,Cart
from cart_app.views import _cart
from store_app.forms import MyForm
from django.contrib import messages
from order_app.models import OrderProduct
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib.auth.decorators import login_required



# Create your views here.
def store(request,category_slug=None):
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Products.objects.all().filter(category=categories,is_available=True).order_by('id')
        paginator=Paginator(products,2)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=products.count()
    else:    
        products=Products.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,6)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=products.count()
    context={
        'products':page_obj,
        'product_count':product_count
    }
    return render(request,'store_app/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product=Products.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(product=single_product,cart__cartid=_cart(request)).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct=OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None
    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)
    product_gallery=ProductGallry.objects.filter(product_id=single_product.id)
    context={
        'product':single_product,
         'in_cart':in_cart,
         'orderproduct':orderproduct,
         'reviews':reviews,
         'product_gallery':product_gallery
    }
    return render(request,'store_app/product_detail.html',context)

def search1(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Products.objects.order_by('created_date').filter(description__icontains=keyword)
            product_count=products.count()
        context={
            'products':products,
            'product_count':product_count,
        }
    return render(request,'store_app/store.html',context)

@login_required(login_url='login')
def review_rating(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=="POST":
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form=MyForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you. Your reviews has been updated!.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=MyForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank You.''Your review has been submitted.')
                return redirect(url)


