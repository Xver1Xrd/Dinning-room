from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from django.db.models import Sum
from django.contrib import messages





from .models import  Size, Category, Item_List, Cart_List, Order

# Create your views here.
def index(request):
	if not request.user.is_authenticated:
		return render(request, "orders/login.html", {"message": None})
	context = {
		"categories" : Category.objects.exclude(name="Topping").all(),
		"items" : Item_List.objects.all(),
		"sizes" : Size.objects.all(),
		"user" : request.user
	}
	return render(request, "orders/index.html", context)
    # return HttpResponse("Project 3: TODO")

def login_view(request):

    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
    	return render(request, "orders/login.html", {"message": "Invalid credentials."})
	# else:
	# return render(request, "orders/login.html")


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def signup_view(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			for msg in form.error_messages:
				print(form.error_messages[msg])
				return render (request = request,
                  template_name = "orders/signup.html",
                  context={"form":form})
	
	form = UserCreationForm        
	return render(request = request,
                  template_name = "orders/signup.html",
                  context={"form":form})

def cart_view(request):
	
	if request.method == "POST":
		item_id = request.POST.get("item_id")
		size = request.POST.get("size_id")
		user = request.user

		p = Item_List.objects.get(pk=item_id)

		# Calculate Price:
		# item = Price_List.objects.get(pk=price_id)


		# if large option selected
		if size and int(size) == 7:
			total_price = p.price
		else:
			total_price = p.price

		# Add new item to cart
		if size == None:
			new_item = Cart_List(user_id=user, item_id=Item_List.objects.get(pk = item_id), size=None, calculated_price=total_price)
		else:
			new_item = Cart_List(user_id=user, item_id=Item_List.objects.get(pk = item_id), size=Size.objects.get(pk = size), calculated_price=total_price)

		# add item to cart
		new_item.save()

		# return HttpResponseRedirect(reverse("cart"))
		messages.success(request, "Блюдо добавлено в корзину!")
		return HttpResponseRedirect(reverse("index"))
		# return render(request, "orders/index.html", {"message": "Meal added to cart!"})

	else:
		try:
			cart = Cart_List.objects.filter(user_id=request.user, is_current=True)
		except Cart_List.DoesNotExist:
			raise Http404("Такого домена еще нет")
		
		total_price = cart.aggregate(Sum('calculated_price'))['calculated_price__sum']

		cart_ordered = Cart_List.objects.filter(user_id=request.user, is_current=False)

		context = {
		"cart_items" : cart,
		"total_price": total_price,
		"cart_items_ordered" : cart_ordered,
		}

		return render(request, "orders/cart.html", context)



def order_view(request):
	# place an order

	if request.method == "POST":
		user = request.user
		items = request.POST.getlist("cart_id")
		print(items)

		new_order = Order(user_id=user)

		new_order.save()

		for item in items:
			new_order.cart_id.add(item)

		# set current attribute to False 
		cart = Cart_List.objects.filter(user_id=request.user)
		for item in cart:
			item.is_current=False
			item.save()
	messages.success(request,"👍 👍🏻 👍🏼 👍🏽 👍🏾 👍🏿")
	return HttpResponseRedirect(reverse("index"))

def removefromcart_view(request, cart_id,):
	# view topping from cart

	item_toremove = Cart_List.objects.get(pk=cart_id)
	item_toremove.delete()
	messages.info(request,"Продукт удален из корзины")
	return HttpResponseRedirect(reverse("Корзина"))

def payment(request,):
	return render(request, "orders/payment.html")
