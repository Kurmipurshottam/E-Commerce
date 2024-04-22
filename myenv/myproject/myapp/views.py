from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import random
import requests

# Create your views here.
def index(request):
    return render(request,"index.html")

def signup(request):
    if request.POST:
        print(">>>>>>>>>>>page lode")
        try:
            user = User.objects.get(email = request.POST['email'])
            print(">>>>>>>>>>>>> User object : ", user)
            msg="Email already exists!"
            messages.error(request, msg)
            return render(request,"signup.html")
        except:
            try:
                if request.POST['password'] == request.POST['cpassword']:
                    user = User.objects.create(
                        first_name = request.POST['first_name'],
                        last_name = request.POST['last_name'],
                        email = request.POST['email'],
                        contact = request.POST['contact'],
                        password = request.POST['password'],
                        user_type = request.POST['user-type'],
                    )
                    print(user.first_name)
                    msg = "Your Registration Done ...."
                    print("============",msg)
                    messages.success(request, msg)
                    return render(request,'login.html')
                    # add ragistration than redirect login page
            except:
                pass
            else:
                msg="Password and Confim Password Does Not Matched !!!"
                messages.error(request, msg)
                return render(request,'signup.html')
    else:
        return render(request,'signup.html')
    
def login(request):
    if request.POST:
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['first_name']=user.first_name  
                request.session['picture']=user.picture.url
                # condition of seller or buyer
                if user.user_type=="buyer":
                    print("hello")
                    msg="Login Successfully"
                    messages.success(request, msg)
                    return redirect('index')
                    # return render(request,"index.html")
                else:
                    print("seller site")
                    msg="Login Successfully"
                    messages.success(request, msg)
                    return redirect('seller_index')
                    # return render(request,"seller_index.html")
                # end seller buyer condition
            else:
                msg="Password does Not Match !!!!"
                messages.error(request, msg)
                return render(request,"index.html")
        except:
            msg="Email Not Ragister Yet !!!"
            messages.error(request, msg)
            return render(request,"login.html")
    else:
        return render(request,"login.html")
    
def change_password(request):
    user=User.objects.get(email=request.session['email'])
    if request.POST:
       print("page lode")
       if user.password == request.POST['old_password']:
           print("======Current password is match")

           if request.POST['new_password1'] == request.POST['new_password2']:
               print("========Page Load new password and conifrm password match =========")
               user.password = request.POST['new_password2']
               user.save()
               msg="Logout Successfully"
               messages.success(request, msg)
               return redirect('logout')
           else:
               print("=============new password and conifrm password doess not match==============")
               msg = "New Password conifrm  password Does not match..."
               messages.error(request,msg)
               if user.user_type=="buyer":
                    return render(request,'change_password.html')
               else:
                    return render(request,'seller_change_password.html')
           
       else:
           print("======Current password does not match")
           msg="Current Password Does not match !!!"
           messages.error(request,msg)
           if user.user_type=="buyer":
                return render(request,'change_password.html')
           else:
                return render(request,'seller_change_password.html')
    else:
        if user.user_type=="buyer":
            return render(request,'change_password.html')
        else:
            return render(request,'seller_change_password.html')
    # return render(request,"change_password.html")

def profile(request):
    print("=============page load=================")
    user = User.objects.get(email = request.session['email'])
    if request.POST:
        print("=============page load 2=================")
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.contact = request.POST['contact']
        if request.POST['picture']:
            user.picture = request.FILES['picture']
        user.save()
        if user.user_type=="buyer":
            return render(request,"index.html")
        else:
            return render(request,"seller_index.html")
    else:
        if user.user_type=="buyer":
            return render(request,"profile.html",{'user':user})
        else:
            return render(request,"seller_profile.html",{'user':user})

def forget_password(request):
    return render(request,"forgetpassword.html")

def forgetpassword_phone(request):
    if request.POST:
        try:
            print("page load")
            user=User.objects.get(contact=request.POST['contact'])
            mobile=request.POST['contact']
            print("mobile = ",mobile)
            otp=random.randint(1001,9999)
            print("otp = ",otp)
            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"P0MKNYqSmOLhjIyp4HDr35nTtsodiwx2uvXcQBa7JVC9g6WE1AGS9KE2gP0cMD3qdI6VRlyZJipe5hAx",
                           "variables_values":str(otp),
                           "route":"otp",
                           "numbers":mobile}

            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response  )
            request.session['mobile'] = mobile
            request.session['otp'] = otp
            msg1="OTP Sent Successfully"
            return render(request,"otp.html",{'msg1':msg1})
        except:
            return render(request,"forgetpassword_phone.html")
    else:
        return render(request,"forgetpassword_phone.html")
    
def otp(request):
    if request.POST:
        otp=int(request.session['otp'])
        uotp=int(request.POST['uotp'])
        print(otp)
        print(uotp)
        if otp==uotp:
            print("hello")
            del request.session['otp']
            return render(request,"reset_password.html")
        else:
            msg="Invalid OTP"
            return render(request,"otp.html",{'msg':msg})
    else:
        return render(request,"otp.html")


def reset_password(request):   
    user=User.objects.get(contact=request.session['mobile']) 
    if request.POST:
        try:
            if request.POST['npassword']==request.POST['ncpassword']:
                user.password=request.POST['ncpassword']
                user.save()
                return render(request,"login.html")
            else:
                msg="New Password and Confirm New Password Does Not Match" 
                return render(request,"reset_password.html",{'msg':msg})       
        except Exception as e:
            print(e)
    else:
        return render(request,"reset_password.html")
    


def shop(request):
    return render(request,"shop.html")

def shoping_cart(request):
    return render(request,"shoping_cart.html")

def home_2(request):
    return render(request,'home_2.html')

def home_3(request):
    return render(request,'home_3.html')

def blog(request):
    return render(request,"blog.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def logout(request):
    del request.session['email']
    del request.session['first_name']
    del request.session['picture']
    print("deleted")
    msg="Logout Successfully"
    messages.success(request, msg)
    return redirect('login')

# seller viwes start 

def seller_index(request):
    return render(request,"seller_index.html")

def add_product(request):
    seller = User.objects.get(email=request.session['email'])
    if request.POST:
        Product.objects.create(
            seller=seller,
            product_category = request.POST['product_category'],
            product_size = request.POST['product_size'],
            product_brand = request.POST['product_brand'],
            price = request.POST['price'],
            product_name = request.POST['product_name'],
            description = request.POST['description'],
            product_picture = request.FILES['product_picture'],
        )
        msg="Product Added Suceesfully"
        return render(request,"add_product.html",{'msg':msg})
    else:
        return render(request,"add_product.html")

def view_product(request):
    seller = User.objects.get(email=request.session['email'])
    product = Product.objects.filter(seller=seller)
    return render(request,"view_product.html",{'product':product})

