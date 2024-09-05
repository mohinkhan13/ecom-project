from django.shortcuts import render,redirect,get_object_or_404
from .models import *
import requests
import random
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.conf import settings
from django.db.models import Count

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'

def validate_email(request):
    email = request.GET.get('email')
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def validate_passwords(request):
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirm_password')
    
    # Check if passwords match
    data = {
        'passwords_match': password == confirm_password
    }
    
    return JsonResponse(data)
# Create your views here.
def index(request):
	best_seller = (Product.objects
               .annotate(total_orders=Count('orderitem'))
               .order_by('-total_orders')[:3])
	hot_trend = (Product.objects
                             .annotate(wishlist_count=Count('wishlist'))
                             .order_by('-wishlist_count')[:3])
	featured_products = Product.objects.filter(is_featured=True)[:3]
	products = Product.objects.all().order_by('-id')[:8]	
	print(hot_trend)
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="buyer":			
			return render(request,'index.html',{'hot_trend':hot_trend,'user':user,'products':products,'best_seller':best_seller,'featured_products':featured_products})
		else:
			return render(request,'seller-index.html',{'user':user})
	except:
		return render(request,'index.html',{'products':products,'best_seller':best_seller,'hot_trend':hot_trend,'featured_products':featured_products})

def login(request):
	if request.method == "POST":
		try:
			user = User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['fname']=user.fname
				request.session['email']=user.email
				request.session['profile_picture']=user.profile_picture.url
				wishlist = Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlist)
				carts = Cart.objects.filter(user=user)
				request.session['cart_counts']=len(carts)
				msg = "Login Successfull"

				if user.usertype == "buyer":					
					return redirect('index')
				else:
					msg = "Login Successfull"
					return render(request,'seller-index.html',{'msg':msg,'user':user})
			else:
				msg = "Password Not Matched"
				return render(request,'login.html',{'msg':msg})
		except User.DoesNotExist:
			msg = "Email Not Found Please Register"
			return render(request, 'register.html', {'msg': msg})
		except Exception as e:
			msg = "An error occurred: " + str(e)
			return render(request, 'login.html', {'msg': msg})
	else:
		return render(request,'login.html')

def register(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg = "Email Already Register"
			return render(request,'login.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_picture=request.FILES['profile_picture'],
					usertype=request.POST['usertype'],
					)
				msg = "Registration Successfull"
				return render(request,'login.html',{'msg':msg})
			else:
				msg = "Password and Confirm Password Not Matched"
				return render(request,'register.html',{'msg':msg})
	else:
		return render(request,'register.html')

def change_password(request):
	user = User.objects.get(email=request.session['email'])
	if request.method=='POST':	
		if request.POST['old_password'] == user.password:
			if request.POST['new_password'] == request.POST['cnew_password']:
				if request.POST['new_password'] != user.password:
					user.password = request.POST['new_password']
					user.save()

					del request.session['email']
					del request.session['fname']
					
					msg = "Password Changed Successfully Please Login Again"					
					return render(request,'login.html',{'msg':msg})					
				else:
					msg = "Old Password And New PassWord Not Be Same"
					if user.usertype=="buyer":
						return render(request,'change-password.html',{'msg':msg})
					else:
						return render(request,'seller-change-password.html',{'msg':msg})
			else:
				msg = "New Password And Confirm New PassWord Must Be Same"
				if user.usertype=="buyer":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})				
		else:
			msg = "Old Password Is Incorrect"
			if user.usertype=="buyer":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'seller-change-password.html',{'msg':msg})
	else:
		try:
			user=User.objects.get(email=request.session['email'])
			if user.usertype=="buyer":
				return render(request,'change-password.html')
			else:
				return render(request,'seller-change-password.html')
		except:
			return render(request,'change-password.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		del request.session['wishlist_count']
		del request.session['cart_counts']
		msg = "User Logout Successfull"
		return render(request,'login.html',{'msg':msg})
	except:
		msg = "User Logout Successfull"
		return render(request,'login.html',{'msg':msg})
		
def profile(request):
	user = User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		request.session['profile_picture']=user.profile_picture.url
		msg = "Your Profile Upadated Successfully"
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		try:
			user=User.objects.get(email=request.session['email'])
			if user.usertype=="buyer":
				return render(request,'profile.html',{'user':user})
			else:
				return render(request,'seller-profile.html',{'user':user})
		except:
			return render(request,'profile.html',{'user':user})
		

def forgot_password(request):
	if request.method=='POST':
		try:
			user = User.objects.get(mobile=request.POST['mobile'])
			mobile = str(user.mobile)
			otp = str(random.randint(100000,999999))
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"TIjv2PHxGFWfdeUqrO5VmSB6MY7Rcnh93ioDutwk0ZaspJAb8QXURP07NkDjvS6HEZVtBCF8MdbYs2n9","variables_values":otp,"route":"otp","numbers":mobile}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			request.session['otp']=otp
			request.session['mobile']=mobile
			return render(request,'otp.html')
		except:
			msg = "Mobile Number Not Register"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')


def verify_otp(request):

	otp1 = int(request.POST['otp'])
	otp2 = int(request.session['otp'])

	if otp1==otp2:
		del request.session['otp']
		return render(request,'new-password.html')
	else:
		msg = "Invalid OTP"
		return render(request,'otp.html',{'msg':msg})


def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user = User.objects.get(mobile=request.session['mobile'])
		user.password=request.POST['new_password']
		user.save()
		del request.session['mobile']
		msg = 'Password Change Successfull'
		return render(request,'login.html',{'msg':msg})
	else:
		msg = 'Password And Confirm Password Not Matched'
		return render(request,'new-password.html',{'msg':msg})


def seller_add_category(request):
    if request.method == 'POST':
        usercate = request.POST['category_name'].lower()
        # Check if the category already exists
        if Category.objects.filter(name=usercate).exists():
            msg = 'Category Already Exists'
            return render(request, 'seller-add-category.html', {'msg': msg})
        else:
            Category.objects.create(name=usercate)
            msg = 'Category Added Successfully'
            return render(request, 'seller-add-category.html', {'msg': msg})
    else:
        return render(request, 'seller-add-category.html')


def seller_product_category(request):
	cat = Category.objects.all()
	return render(request,'seller-product-category.html',{'cat':cat})



def seller_add_product(request):
    cat = Category.objects.all()
    if request.method == "POST":
        seller = User.objects.get(email=request.session['email'])
        category = Category.objects.get(name=request.POST['product_category'])  # Use the ID instead of name
        
        Product.objects.create(
            seller=seller,
            product_name=request.POST['product_name'],
            product_category=category,  # Assign the Category instance directly
            product_price=request.POST['product_price'],
            highlight_price=request.POST['highlight_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image'],
        )
        msg = "Product Added Successfully"
        return render(request, 'seller-add-product.html', {'msg':msg, 'cat':cat})
    else:
        return render(request, 'seller-add-product.html', {'cat':cat})

def delete_category(request,id):
	category = Category.objects.get(id=id)
	category.delete()
	return redirect('seller-product-category')

def seller_product(request):
	seller=User.objects.get(email=request.session['email'])
	product = Product.objects.filter(seller=seller).order_by('-id')
	total_products = product.count()
	return render(request,'seller-product.html',{'product':product,'total_products':total_products})


def seller_view_product(request,id):
	product = Product.objects.get(pk=id)	
	return render(request,'seller-view-product.html',{'product':product})

def seller_edit_product(request,id):
	product = Product.objects.get(pk=id)
	cat = Category.objects.all()

	if request.method=="POST":
		category_name = request.POST.get('product_category')
		if category_name:
			category = Category.objects.get(name=request.POST['product_category']) 
			product.product_category = category
		product.product_name = request.POST['product_name']	
		product.is_featured = request.POST['is_featured']	
		product.product_price = request.POST['product_price']
		product.highlight_price=request.POST['highlight_price']
		product.product_desc = request.POST['product_desc']
		try:
			product.product_image = request.FILES['product_image']
		except:
			pass
		product.save()
		msg = "Product Detail Updated"
		return render(request,'seller-edit-product.html',{'msg':msg,'product':product,'cat':cat})
	else:
		return render(request,'seller-edit-product.html',{'product':product,'cat':cat})

def seller_delete_product(request,id):
	product = Product.objects.get(pk=id)	
	product.delete()
	msg = 'Product Delete Successfully'
	return redirect('seller-product')

def product_detail(request,id):
	product = Product.objects.get(id=id)
	category = product.product_category
	filter_products = Product.objects.filter(product_category=category).exclude(id=product.id)[:4]
	return render(request,'product-details.html',{'product':product,'filter_products':filter_products})

def category_products(request,cate):
	cat = Category.objects.all()
	if cate == 'all':
		products = Product.objects.all().order_by('-id')
		return render(request,'category-products.html', {'category':cate,'products': products})
	category = get_object_or_404(Category, name=cate)
	products = Product.objects.filter(product_category=category).order_by('-id')
	return render(request,'category-products.html',{'cat':cat,'category': category,'products':products})

def wishlist(request):
    # Check if the user is authenticated
    if 'email' not in request.session:
        return redirect('login')  # Redirect to login page if the user is not logged in

    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        return redirect('login')  # Redirect to login page if the user is not found

    # Fetch the wishlist items for the user
    wishlist = Wishlist.objects.filter(user=user)
    request.session['wishlist_count']=len(wishlist)
    
    return render(request, 'wishlist.html', {'wishlist': wishlist})

def user_wishlist(request, id):
	try:
	    product = Product.objects.get(id=id)
	    user = User.objects.get(email=request.session['email'])
	    if not Wishlist.objects.filter(user=user, product=product).exists():
	        # Add the product to the wishlist if it's not already there
	        Wishlist.objects.create(user=user, product=product)

	    return redirect('wishlist')

	except:
		msg = "Please Login For Add Itme in Wishlist"
		return render(request,'login.html', {'msg':msg})

def remove_wishlist(request,id):
	product = Product.objects.get(id=id)
	user = User.objects.get(email=request.session['email'])
	wishlist = Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def cart(request):
    if 'email' not in request.session:
        return redirect('login')  # Redirect to login page if the user is not logged in
    try:
        user = User.objects.get(email=request.session['email'])
    except User.DoesNotExist:
        return redirect('login')  # Redirect to login page if the user is not found

    # Fetch the wishlist items for the user
    net_price=0
    carts = Cart.objects.filter(user=user,payment_status=False)
    for i in carts:
    	net_price += i.total_price
    request.session['cart_counts']=len(carts)
    
    return render(request, 'cart.html', {'carts': carts, 'net_price':net_price, 'user':user})

def user_cart(request, id):
	try:
	    product = Product.objects.get(id=id)
	    user = User.objects.get(email=request.session['email'])
	    if not Cart.objects.filter(user=user, product=product).exists():
	        # Add the product to the wishlist if it's not already there
	        Cart.objects.create(
				user=user,
				product=product,
				product_price=product.product_price,
				product_qty=1,
				total_price=product.product_price,
				payment_status=False
			)

	    return redirect('cart')

	except:
		msg = "Please Login For Add Itme in Wishlist"
		return render(request,'login.html', {'msg':msg})

def remove_cart(request,id):
	product = Product.objects.get(id=id)
	user = User.objects.get(email=request.session['email'])
	cart = Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')


def change_qty(request):
    print(request.POST)  # Add this line to see the POST data
    product_qty = int(request.POST.get('product_qty'))
    cid = int(request.POST.get('cid'))

    try:
        cart = Cart.objects.get(pk=cid)
        cart.product_qty = product_qty
        cart.total_price = cart.product_price * product_qty
        cart.save()
    except Cart.DoesNotExist:
        # Handle the case where the cart item does not exist
        pass

    return redirect('cart')


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = request.session.get('email', 'guest@example.com')  # Fallback if email is not in session
        amount = int(data['post_data'])        
        final_amount = amount * 100

        user = User.objects.get(email=request.session['email'])
        
        user_name = f"{user.fname} {user.lname}"
        user_address = f"{user.address}"
        user_mobile = f"{user.mobile}"
        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': final_amount,
                    'product_data': {
                        'name': 'Checkout Session Data',
                        'description': f'''Customer: {user_name},\n\n 
                        Address: {user_address}, \n 
                        Mobile: {user_mobile}''',
                    },
                    
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + f'/payment-success/{{CHECKOUT_SESSION_ID}}/',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            customer_email=email,
            shipping_address_collection={
                'allowed_countries': ['IN'],
            },
        )

        return JsonResponse({'id': session.id})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def payment_success(request, session_id):
    try:
        # Stripe se payment session ki details fetch karein
        session = stripe.checkout.Session.retrieve(session_id)
        customer_email = session.get('customer_email')
        payment_status = session.get('payment_status')
        
        # User ko retrieve karein email se
        user = get_object_or_404(User, email=customer_email)

        if payment_status == 'paid':
            # Agar payment successful ho, to Order entry create karein
            order = Order.objects.create(
                user=user,
                full_name=f"{user.fname} {user.lname}",
                address=user.address,
                mobile=user.mobile,
                total_amount=session['amount_total'] / 100,  # paisa ko INR me convert karen
                status='paid'
            )
            
            # User ke cart items ko fetch karein jo abhi tak paid nahi hain
            user_cart_items = Cart.objects.filter(user=user, payment_status=False)
           
            # Order items ko create karein aur Cart items ko delete karein
            for item in user_cart_items:
                OrderItem.objects.create(
                	seller=item.product.seller,
                    order=order,
                    product=item.product,
                    product_qty=item.product_qty,
                    product_price=item.product_price,
                    total_price=item.total_price
                )
            
            # Cart items ko delete karein
            user_cart_items.delete()

            # Cart count ko session mein update karein
            request.session['cart_counts'] = 0

            # Order success page render karein
            return render(request, 'order_success.html', {'order': order})
        else:
            return HttpResponse("Payment not successful")
    
    except stripe.error.StripeError as e:
        # Stripe se related error ko handle karein
        return HttpResponse(f"Stripe Error: {str(e)}", status=400)
    
    except Exception as e:
        # Any other error ko handle karein
        return HttpResponse(f"Error occurred: {str(e)}", status=500)



def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_counts']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def order_list(request):
	try:
		user = User.objects.get(email=request.session['email'])
		orders = Order.objects.filter(user=user).order_by('-created_at')
		return render(request,'order-list.html', {'orders':orders})
	except:
		return render(request,'order-list.html')

def order_detail(request,order_id):
	user = User.objects.get(email=request.session['email'])
	order = Order.objects.get(id=order_id)
	return render(request,'order-detail.html', {'order':order})

def contact(request):
	return render(request,'contact.html')

def about(request):
	return render(request,'about.html')

def seller_orders(request):
	seller = User.objects.get(email=request.session['email'])
	orders = Order.objects.filter(items__seller=seller).distinct()
	return render(request,'seller-orders.html',{'orders':orders})

def seller_order_detail(request, order_id):
    seller = User.objects.get(email=request.session['email'])
    order = get_object_or_404(Order.objects.filter(id=order_id, items__seller=seller).distinct())

    context = {
        'order': order,
    }
    return render(request, 'seller_order_detail.html', context)

def seller_inventory(request):
	seller = User.objects.get(email=request.session['email'])
	products = Product.objects.filter(seller=seller).prefetch_related('inventory_set')
	return render(request,'seller-inventory.html',{'products':products})

def update_inventory(request, id):
    item = get_object_or_404(Inventory, id=id)
    
    if request.method == 'POST':
        stock = request.POST.get('stock')
        try:
            stock = int(stock)  # Convert to integer
            item.stock = stock
            item.save()
        except ValueError:
            # Handle the case where stock is not a valid integer
            return render(request, 'update-inventory.html', {'item': item, 'error': 'Invalid stock value'})
        return redirect('seller-inventory')  # Redirect to the inventory list page
    else:
        return render(request, 'update-inventory.html', {'item': item})