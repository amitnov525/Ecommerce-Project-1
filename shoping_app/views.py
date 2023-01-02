from pyexpat.errors import messages
from django.shortcuts import render,redirect
from store_app.models import Products
from store_app.models import ReviewRating
from shoping_app.forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from ecommerce import wsgi
# Create your views here.
def home(request):
    products=Products.objects.all().filter(is_available=True)
    for product in products:
        reviews=ReviewRating.objects.filter(product_id=product.id,status=True)
    context={
        'products':products,
        'reviews':reviews
    }
    return render(request,'shoping_app/home.html',context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
                subject = "Website Inquiry" 
                body = {
			    'first_name': form.cleaned_data['first_name'], 
			    'last_name': form.cleaned_data['last_name'], 
			    'email': form.cleaned_data['email_address'], 
			    'message':form.cleaned_data['message'], 
			    }
                from_email=body.get('email')
                to_email=['amit170111nov@gmail.com']
                message = "\n".join(body.values())
                try:
                    send_mail(subject, message, from_email, to_email) 
                    messages.success(request,'ThanK You We have received Your form. We will get back to You soon.')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect ("contact")
    form = ContactForm()
    return render(request, "shoping_app/contact.html", {'form':form})
