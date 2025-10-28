from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as trouble
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, SearchForm, ProductEditForm
from django.contrib.auth.decorators import login_required
import random 
from . models import Category, Products, Cart, WishList, Checkout, User, DefaultImages
from django.views.generic import UpdateView
from web.utils.login import user_is_superuser_or_staff
from django_daraja.views import stk_push_success
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer

"""
API VIEWS
"""

class ProductListView(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

"""
WEB VIEWS
"""

def start():
    int = random.randint(1,150)
    return int
def step():
    int = random.randint(9,25)
    return int
def stop():
    int = random.randint(155,160)
    return int

activeProducts = Products.objects.filter(active=True)
products = Products.objects.all()
countableCategories = Category.objects.annotate(count=Count('product'))
categories = Category.objects.all()
image = DefaultImages.objects.first()

def categoryData(categoryqueryset):
    dic = {}
    for item in categoryqueryset:
        dic[item] = categoryqueryset.get(name=item.name).product.all()
    return dic

data = {"products":products,
        "defaultimage":image,
        "categoryz":categories[:6],
        "category":categories,
        "countableCategories":countableCategories,
        }

def view404(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, '404.html')

def about(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'about.html')

@login_required
def cart(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = cart.product.all()
    return render(request, 'cart.html',{'product':product,'data':data})

def category_view(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    data["neatCategory"] = categoryData(data['countableCategories'])
    return render(request, 'basecategory.html', data)

def category(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    data['cat'] = Category.objects.filter(name=name).first()
    data['product'] = Products.objects.filter(category=data['cat'])
    data['categorys'] = Category.objects.all()
    data["neatCategory"] = categoryData(data['countableCategories'])
    return render(request, 'category.html', data)

@login_required
def checkout(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    checkout, created = Checkout.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    products = checkout.product.all()
    return render(request, 'checkout.html', {'products':products})

def comingSoon(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'coming-soon.html')

def contact(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'contact.html')

@login_required
def dashboard(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'dashboard.html')

def index13(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    data['products'] = products[start():stop():step()]
    data['search'] = SearchForm(request.GET)
    return render(request, 'index-13.html', data)

def index(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'index.html')

def login_view(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    creation_form = CustomUserCreationForm()
    login_form = CustomLoginForm()

    if request.method == "POST":
        if "register" in request.POST:
            creation_form = CustomUserCreationForm(request.POST)
            if creation_form.is_valid():
                username = creation_form.cleaned_data.get('username')
                email = creation_form.cleaned_data.get('email')
                password1 = creation_form.cleaned_data.get('password1')

                user = User.objects.create_user(username=username, email=email, password=password1)
                
                trouble(request, user)  # Log in the user after registration
                messages.success(request, "Registration successful!")
                return redirect('/home/')  # Change 'home' to your homepage URL
            else:
                messages.error(request, f"Please correct the errors below.")
                return render(request, 'login.html', {'login_form':login_form,'creation_form':creation_form})
                            
        elif "login" in request.POST:
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    trouble(request,user)
                    messages.success(request, f"Welcome {username}!")
                    return redirect('/home/')  # Change 'home' to your actual homepage URL name
                else:
                    messages.error(request, "User is not registered")
            else:
                messages.error(request, "Invalid username or password for login")
                return render(request, 'login.html', {'login_form':login_form,'creation_form':creation_form})
    else:
        creation_form = CustomUserCreationForm()
        login_form = CustomLoginForm()
        return render(request, 'login.html', {'login_form':login_form,'creation_form':creation_form})

def productCategoryFullwidth(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    return render(request, 'product-category-fullwidth.html')

def product(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    data['product'] = products.filter(name=name).first()
    data['products'] = products[start():stop():step()]
    return render(request, 'product.html', data)

def wishlist(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        products = wishlist.product.all()
        return render(request, 'wishlist.html', {'products':products,'data':data})
    else:
        wishlist, created = WishList.objects.get_or_create(user=None)
        products = wishlist.product.all()
        return render(request, 'wishlist.html', {'products':products})
    

def user_logout(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/login/')

@login_required
def add_to_cart(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    product = Products.objects.get(name=name)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product in cart.product.all():
        messages.info(request, f"you already have this in your cart!")
    else:
        cart.product.add(product)
        cart.save()
        messages.success(request, f"{product} added to cart!")
    return redirect('/home/')

def remove_from_cart(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    product = Products.objects.get(name=name)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart.product.remove(product)
    cart.save() 
    messages.warning(request, f"{product} removed from cart!") 
    return redirect('/cart/') 

def add_to_wishlist(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    product = Products.objects.get(name=name)
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.product.add(product)
        wishlist.save()
        messages.success(request, f"{product} added to wishlist!")
        return redirect('/home/')
    else:
        wishlist, created = WishList.objects.get_or_create(user=None)
        wishlist.product.add(product)
        messages.success(request, f"{product} added to wishlist!")
        return redirect('/home/')

def remove_from_wishlist(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    product = Products.objects.get(name=name)
    wishlist, created = WishList.objects.get_or_create(user=request.user if request.user.is_authenticated else None)

    wishlist.product.remove(product)
    wishlist.save() 
    messages.warning(request, f"{product} removed from wishlist!") 
    return redirect('/wishlist/') 

@login_required
def cart_from_wishlist(request,name):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    add_to_cart(request=request,name=name)
    remove_from_wishlist(request=request,name=name)
    return redirect('/cart/') 

@login_required
def add_to_checkout(request):
    data["cart"] = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    cart_item, created = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    products = [item.id for item in cart_item.product.all()]
    checkout, created = Checkout.objects.get_or_create(user=request.user if request.user.is_authenticated else None)

    checkout.product.add(*products)
    cart_item.product.remove(*products)
    cart_item.save()
    checkout.save
    messages.success(request, 'products added to checkout')
    return redirect('/checkout/')

def search_product(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            # Process the form and handle the search
            name = form.cleaned_data['search']
            data["product"] = products.filter(name__contains=name)
    else:
        form = SearchForm()
        data['defaultimage'] = DefaultImages.objects.first()

    return render(request, 'category-boxed.html', data)


# A function-based view (FBV) to update the product
@user_is_superuser_or_staff
def edit_product(request, pk):
    product = get_object_or_404(Products, pk=pk)
    
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'{product.name} edited successfully')
            return redirect('/home/')  # Redirect to a success page after save
    else:
        form = ProductEditForm(instance=product)    
    return render(request, 'product_edit.html', {'form': form, 'product': product, 'data':data})

def checkout_test(request):
    return stk_push_success(request)


## tools ##

'''
view for listing products
'''
@user_is_superuser_or_staff
def listProducts(request):
    return render(request, 'listproducts.html', {'products':products})


'''
function for disabling products without pictures
'''
@user_is_superuser_or_staff
def disableWoutPic(request):
    for item in products:
        if not item.image :
            item.active = False
            item.save()
   # messages.success(request, f'{item} edited successfully')
    return redirect('/home/')  # Redirect to a success page after save