from base64 import urlsafe_b64decode
from email import message
from django.shortcuts import get_object_or_404, render,redirect
from accounts.forms import RegistrationForm, UserForm,UserProfileForm
from accounts.models import MyUser, UserProfile
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from cart_app.views import _cart
from cart_app.models import CartItem,Cart
from urllib.parse import urlparse
from order_app.models import Order,OrderProduct

# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=MyUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            current_site=get_current_site(request)
            mail_subject="Please Activate Your Account"
            message=render_to_string('accounts/account_verification.html', {'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
                })
            to_email=email 
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    context={
            'form':form
        }
    return render(request,'accounts/register.html',context)

def login_user(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cartid=_cart(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items=CartItem.objects.filter(cart=cart)
                    product_variation=[]
                    for item in cart_items:
                        variation=item.variation.all()
                        product_variation.append(list(variation))
                    cart_item=CartItem.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_vartion=item.variation.all()
                        ex_var_list.append(list(existing_vartion))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            id1=id[index]
                            item=CartItem.objects.get(id=id1)
                            item.quantity=item.quantity+1
                            item.user=user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user 
                                item.save()
                            
            except:
                pass
            login(request,user)
            messages.success(request,'You are logged in')
            url=request.META.get('HTTP_REFERER')
            try:
                path=urlparse(url)
                query1=path.query
                parms=dict(x.split("=") for x in query1.split('&'))
                print(parms)
                if 'next' in parms:
                    nextpage=parms['next']
                    return redirect(nextpage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request,'Ivalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,'You are Logged Out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=MyUser._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,MyUser.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True 
        user.save()
        id1=user.id
        messages.success(request,'Congratulations Registration Successfull Please Complete Your Profile.')
        return redirect('createprofile',id1)
    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    try:
        userprofile=UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        userprofile=None
    context={
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request,'accounts/dasboard.html',context)

def forgot_password(request):
    if request.method=="POST":
        email=request.POST['email']
        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="PLEASE RESET YOUR PASSWORD"
            message=render_to_string('accounts/reset_password_email.html',
            {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email=email 
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password Reset Mail has been sent to your mail')
            return redirect('login')
        else:
            messages.error(request,'Email Does not exist')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=MyUser._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,MyUser.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid 
        messages.success(request,'Please Reset Your Password')
        return redirect('reset_password')
    else:
        messages.error(request,'Eiether invlid link or link expired')
        return redirect('login')

def reset_password(request):
    if request.method=="POST":
        password=request.POST['password']
        password1=request.POST['confirm_password']
        if password==password1:
            uid=request.session['uid']
            user=MyUser.objects.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Changed Successfully |')
            return redirect('login')
        else:
            messages.error(request,'Password does not match')
            return redirect('reset_password')
    else:
        return render(request,'accounts/resetpassword.html')

@login_required(login_url='login')
def change_password(request):
    if request.method=="POST":
        password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        if new_password==confirm_password:
            id=request.user.id
            user=MyUser.objects.get(id=id)
            success=user.check_password(password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Changed Successfully.Please Login')
                return redirect('login')
            else:
                messages.error(request,'Please Enter Your Correct Current  Password')
                return redirect('change_password')

        else:
            messages.error(request,'Password does not match. Please Try Again.')
            return redirect('change_password')
    else:
        return render(request,'accounts/changepassword.html')

@login_required(login_url='login')    
def myorders(request):
    orders=Order.objects.filter(user_id=request.user.id,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders
    }

    return render(request,'accounts/myorder.html',context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    print(userprofile,'******************')
    if request.method=="POST":
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'You Profile has been updated')
            return redirect('edit-profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile
    }
    return render(request,'accounts/editprofile.html',context)

def createprofile(request,id):
    user=get_object_or_404(MyUser,id=id)
    if request.method=="POST":
        print("Inside Post")
        profile_form=UserProfileForm(request.POST,request.FILES)
        
        if profile_form.is_valid():
            print("Print Inside Form Valids")
            pf=profile_form.save(commit=False)
            pf.user_id=user.id
            pf.save()
            messages.success(request,'You Profile has Created')
            print("Rediecting")
            return redirect('login')
    else:
        profile_form=UserProfileForm()
    context={
        'profile_form':profile_form,
        'user':user
    }
    return render(request,'accounts/createprofile.html',context)


@login_required(login_url='login')
def order_detail(request,order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    subtotal=0
    for item in order_detail:
        subtotal+=item.product_price*item.quantity
    context={
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal
    }
    return render(request,'accounts/order_detail.html',context)

    






