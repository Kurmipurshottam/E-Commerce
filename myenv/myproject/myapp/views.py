from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import random
import requests
from django.conf import settings
import razorpay
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def index(request):
    try:
        user = User.objects.get(email = request.session['email'])
        if user.user_type=="buyer":
            return render(request,"index.html")
        else:
            return render(request,'seller_index.html')
    except:
        return render(request,"index.html")

@never_cache
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

@never_cache    
def login(request):
    if request.POST:
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                if user.user_type=="buyer":
                    # condition of seller or buyer
                    request.session['email']=user.email
                    request.session['first_name']=user.first_name  
                    request.session['picture']=user.picture.url
                    try:
                        request.session['wishlist']=len(wishlist)
                        request.session['cart']=len(shoping_cart)
                    except Exception as e:
                        print(e)
                    print(wishlist)
                    print("hello")
                    pmsg="Login Successfully"
                    messages.success(request,pmsg)
                    return redirect('index')
                    # return render(request,"index.html")
                else:
                    # condition of seller or buyer
                    request.session['email']=user.email
                    request.session['first_name']=user.first_name  
                    request.session['picture']=user.picture.url
                    print("seller site")
                    msg="Login Successfully"
                    messages.success(request,msg)
                    return redirect('seller_index')
                    # return render(request,"seller_index.html")
                # end seller buyer condition
            else:
                msg="Password does Not Match !!!!"
                messages.error(request,msg)
                return render(request,"login.html")
        except:
            msg="Email Not Ragister Yet !!!"
            messages.error(request,msg)
            return render(request,"login.html")
    else:
        return render(request,"login.html")

@never_cache   
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
               pmsg = "New Password conifrm  password Does not match..."
               messages.error(request,pmsg)
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

@never_cache
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
        msg="profile updated successfuly"
        messages.success(request,msg)
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

@never_cache
def forget_password(request):
    return render(request,"forgetpassword.html")

@never_cache
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
            msg="OTP Sent Successfully"
            messages.success(request,msg)
            return render(request,"otp.html")
        except:
            return render(request,"forgetpassword_phone.html")
    else:
        return render(request,"forgetpassword_phone.html")

@never_cache   
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
            messages.error(request,msg)
            return render(request,"otp.html")
    else:
        return render(request,"otp.html")

@never_cache
def reset_password(request):   
    user=User.objects.get(contact=request.session['mobile']) 
    if request.POST:
        try:
            if request.POST['npassword']==request.POST['ncpassword']:
                user.password=request.POST['ncpassword']
                user.save()
                msg="password reset successfuly" 
                messages.success(request,msg)
                return render(request,"login.html")
            else:
                msg="New Password and Confirm New Password Does Not Match" 
                messages.error(request,msg)
                return render(request,"reset_password.html")       
        except Exception as e:
            print(e)
    else:
        return render(request,"reset_password.html")

@never_cache
def shop(request,cat):
    if cat=="all":
        product=Product.objects.all()
    elif cat=="women":
        product=Product.objects.filter(product_category="Women")
    elif cat=="men":
        product=Product.objects.filter(product_category="Men")
    elif cat=="child":
        product=Product.objects.filter(product_category="Child")
    return render(request,"shop.html",{'product':product})

@never_cache
def buyer_product_details(request,pk):
    wishlist_flag=False
    cart_flag=False
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_flag=True
    except:
        pass
    try:
        Cart.objects.get(user=user,product=product)
        cart_flag=True
    except:
        pass
    print("==========================##################@@@@@@@@@@@@@@@@@@@@@@@",product)
    return render(request,'buyer_product_details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

@never_cache
def home_2(request):
    return render(request,'home_2.html')

@never_cache
def home_3(request):
    return render(request,'home_3.html')

@never_cache
def blog(request):
    return render(request,"blog.html")

@never_cache
def about(request):
    return render(request,"about.html")

@never_cache
def contact(request):
    return render(request,"contact.html")

@never_cache
def logout(request):
    del request.session['email']
    del request.session['first_name']
    del request.session['picture']
    try:
        del request.session['total']
        del request.session['wishlist']
        del request.session['cart']
        print("===============================",request.session['wishlist'])
    except Exception as e:
        print("=============================================",e)
    print("deleted")
    msg="Logout Successfully"
    messages.success(request, msg)
    return redirect('login')

@never_cache
def add_to_wishlist(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    Wishlist.objects.create(user=user,product=product)
    return redirect("wishlist")

@never_cache
def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.filter(user=user)
    request.session['wishlist']=len(wishlist)
    return render(request,"wishlist.html",{'wishlist':wishlist})

@never_cache
def delete_wishlist(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    wishlist=Wishlist.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect("wishlist")

@never_cache
def add_to_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    Cart.objects.create(user=user,
                        product=product,
                        cart_price=product.price,
                        total_price=product.price,
                        quantity=1
                        )
    return redirect("shoping_cart")

@never_cache
def shoping_cart(request):
    if not request.session['email']:
        msg="Please login first!!!"
        messages.info(request,msg)
        return render(request,"shop.html")
        
    else:
        subtotal=0
        ship=0
        user=User.objects.get(email=request.session['email']) 
        cart=Cart.objects.filter(user=user)
        request.session['cart']=len(cart)
        # print("======================",request.session['cart'])
        for i in cart:
            subtotal+=i.total_price
        if subtotal<=20000:
            ship=100
            total=subtotal+ship
        else:
            total=subtotal
        request.session['total'] = total
        return render(request,"shoping_cart.html",{'cart':cart,'subtotal':subtotal,'ship':ship,'user':user,'total':total})

@never_cache    
def delete_cart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    cart=Cart.objects.get(user=user,product=product)
    cart.delete()
    return redirect("shoping_cart")

@never_cache
def change_quantity(request,pk):
    cart=Cart.objects.get(pk=pk)
    cart.quantity=int(request.POST['qty'])
    request.session['cart_quantity'] = cart.quantity
    print("Cart Quantity in session:", request.session.get('cart_quantity'))
    cart.save()
    cart.total_price=cart.cart_price*cart.quantity
    
    cart.save()
    return redirect("shoping_cart") 

@never_cache
def order_details(request):
    user=User.objects.get(email=request.session['email'])
    if request.POST:
        try:
            order_details = Order_details.objects.create(
                user=user,
                address = request.POST['address'],
                pincode = request.POST['pincode']  
            )
            order_details.save()
            return redirect("check_out")
        except:
            return redirect("check_out")
        
    else:
        return render(request,"check_out.html")

@never_cache
def check_out(request):
    user=User.objects.get(email=request.session['email'])
    order=Order_details.objects.filter(user=user)
    cart=Cart.objects.filter(user=user)
    total=request.session['total']
    print("================",total)

    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': total * 100, 'currency': 'INR', 'payment_capture': 1})
    context = {
        'payment': payment,
        }
    print("=======================",context)
    print("&7777777777777777777777",payment)
    
    return render(request,"check_out.html",{'user':user,'order':order,'context':context})

@never_cache
def success(request):
    try:
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user,pyment_status=False)

        for i in cart:
            i.pyment_status=True
            i.save()
        return render(request,"success.html",{'cart':cart})
    except:
        return redirect("index")

# def order(request):
#     user=User.objects.get(email=request.session['email'])
#     if request.session['email']:
#         if request.POST:
#             order = Order.objects.create(
#                     user=user,
#                     address = request.POST.get('address'),
#                     pincode = request.POST.get('pincode'),
#                     contact = request.POST.get('contact'),
#                     total_price = request.POST.get('total_price')
#                 )
#             order.save()
#             return redirect('check_out')
        
# def delete_address(request):
#     if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         address_id = request.POST.get('id')
#         try:
#             order_details = Order_details.objects.get(id=address_id)
#             order_details.delete()
#             return JsonResponse({'message': 'Address deleted successfully'}, status=200)
#         except Order_details.DoesNotExist:
#             return JsonResponse({'error': 'Address not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)
# # seller viwes start 

@never_cache
def seller_index(request):
    return render(request,"seller_index.html")

@never_cache
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
        messages.success(request,msg)
        return render(request,"add_product.html")
    else:
        return render(request,"add_product.html")

@never_cache
def view_product(request):
    seller = User.objects.get(email=request.session['email'])
    product = Product.objects.filter(seller=seller)
    return render(request,"view_product.html",{'product':product})

@never_cache
def product_details(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,"product_details.html",{'product':product})

@never_cache
def product_edit(request,pk):
    product=Product.objects.get(pk=pk)
    if request.POST:
        product.product_category = request.POST['product_category']
        product.product_size = request.POST['product_size']
        product.product_brand = request.POST['product_brand']
        product.price = request.POST['price']
        product.product_name = request.POST['product_name']
        product.description = request.POST['description']
        try:
                product.product_picture = request.FILES['product_picture']
        except:
            pass
        product.save()
        msg="Product Updated Suceesfully"
        messages.success(request,msg)
        return render(request,"product_edit.html",{'product':product})
    else:
        return render(request,"product_edit.html",{'product':product})

@never_cache
def product_delete(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    msg="Product Deleted Suceesfully"
    messages.success(request,msg)
    return redirect('view_product')

