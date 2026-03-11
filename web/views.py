from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, SearchForm, ProductEditForm, AddToCart, ProfileForm, UserDetailsForm, ShippingAddressForm
from django.contrib.auth.decorators import login_required
from . models import Category, Products, Cart, WishList, Checkout, User, Profile, Order
from web.utils.login import user_is_superuser_or_staff
from django_daraja.views import stk_push_success

from .context_helpers import get_base_context, get_cart_products, get_category_products

def view404(request):
    context = get_base_context(request)
    return render(request, '404.html', context)

def about(request):
    context = get_base_context(request)
    return render(request, 'about.html', context)

@login_required
def cart(request):
    context = get_base_context(request)
    cart_obj = get_cart_products(request)
    context['products'] = cart_obj.product.all()
    return render(request, 'cart.html', context)

def category_view(request):
    context = get_base_context(request)
    context['products'] = Products.objects.all()
    context['categories'] = Category.objects.all()
    context['category_products'] = get_category_products(context['countable_categories'])
    return render(request, 'basecategory.html', context)

def category(request, name):
    context = get_base_context(request)
    cat = Category.objects.filter(name=name).first()
    context['current_category'] = cat
    context['products'] = Products.objects.filter(category=cat) if cat else Products.objects.none()
    context['categories'] = Category.objects.all()
    context['category_products'] = get_category_products(context['countable_categories'])
    return render(request, 'category.html', context)

@login_required
def checkout(request):
    context = get_base_context(request)
    checkout_obj, _ = Checkout.objects.get_or_create(user=request.user)
    context['products'] = checkout_obj.product.all()
    context['subs'] = checkout_obj.subtotals()
    return render(request, 'checkout.html', context)

def comingSoon(request):
    context = get_base_context(request)
    return render(request, 'coming-soon.html', context)

def contact(request):
    context = get_base_context(request)
    return render(request, 'contact.html', context)

@login_required
def dashboard(request):
    context = get_base_context(request)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserDetailsForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Account details updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserDetailsForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    # Get user's orders and last one for shipping address
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    last_order = orders.first()
    
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['orders'] = orders
    context['last_shipping_address'] = last_order.shipping_address if last_order else None
    context['last_phone_number'] = last_order.phone_number if last_order else None
    return render(request, 'dashboard.html', context)

def index13(request):
    context = get_base_context(request)
    context['products'] = Products.objects.all()[:6]
    context['search'] = SearchForm(request.GET)
    context['cartform'] = AddToCart(request.GET)
    return render(request, 'index-13.html', context)

def index(request):
    context = get_base_context(request)
    return render(request, 'index.html', context)

def login_view(request):
    context = get_base_context(request)
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
                
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('/home/')
            else:
                messages.error(request, f"Please correct the errors below.")
                context['login_form'] = login_form
                context['creation_form'] = creation_form
                return render(request, 'login.html', context)
                            
        elif "login" in request.POST:
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome {username}!")
                    return redirect('/home/')
                else:
                    messages.error(request, "User is not registered")
            else:
                messages.error(request, "Invalid username or password for login")
                context['login_form'] = login_form
                context['creation_form'] = creation_form
                return render(request, 'login.html', context)
    else:
        creation_form = CustomUserCreationForm()
        login_form = CustomLoginForm()
        context['login_form'] = login_form
        context['creation_form'] = creation_form
        return render(request, 'login.html', context)

def productCategoryFullwidth(request):
    context = get_base_context(request)
    return render(request, 'product-category-fullwidth.html', context)

def product(request, name):
    context = get_base_context(request)
    product_obj = Products.objects.filter(name=name).first()
    context['product'] = product_obj
    context['related_products'] = Products.objects.all()[:6]
    return render(request, 'product.html', context)

def wishlist(request):
    return redirect('notfound')
    context = get_base_context(request)
    if request.user.is_authenticated:
        wishlist_obj, _ = WishList.objects.get_or_create(user=request.user)
    else:
        wishlist_obj, _ = WishList.objects.get_or_create(user=None)
    
    context['products'] = wishlist_obj.product.all()
    return render(request, 'wishlist.html', context)
    

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/login/')

@login_required
def add_to_cart(request, name):
    form = AddToCart(request.GET)
    product = Products.objects.get(name=name)
    cart = Cart.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        form = AddToCart(request.GET)
        if form.is_valid():
            amount = form.cleaned_data['order_amount']
            if False in cart:
                if product in cart[0].product.all():
                    messages.info(request, f"you already have this in your cart!")
                else:
                    cart[0].product.add(product)
                    cart_product = cart[0].product.filter(name=name).first()
                    cart_product.order_amount = amount
                    cart_product.save()
                    messages.success(request, f"{product} added to cart!")

        else:
            raise ValueError("Invalid form data for adding to cart")
    else:
        raise ValueError("Invalid request method for adding to cart")

    return redirect('/home/', {'form': form})

def update_cart_amount():
    # ToDo : add cart update logic
    pass

def remove_from_cart(request, name):
    product = Products.objects.get(name=name)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart.product.remove(product)
    cart.save() 
    messages.warning(request, f"{product} removed from cart!") 
    return redirect('/cart/') 

def add_to_wishlist(request, name):
    product = Products.objects.get(name=name)
    if request.user.is_authenticated:
        wishlist, _ = WishList.objects.get_or_create(user=request.user)
    else:
        wishlist, _ = WishList.objects.get_or_create(user=None)
    
    wishlist.product.add(product)
    wishlist.save()
    messages.success(request, f"{product} added to wishlist!")
    return redirect('/home/')

def remove_from_wishlist(request, name):
    product = Products.objects.get(name=name)
    wishlist, _ = WishList.objects.get_or_create(user=request.user if request.user.is_authenticated else None)

    wishlist.product.remove(product)
    wishlist.save() 
    messages.warning(request, f"{product} removed from wishlist!") 
    return redirect('/wishlist/') 

@login_required
def cart_from_wishlist(request, name):
    add_to_cart(request=request, name=name)
    remove_from_wishlist(request=request, name=name)
    return redirect('/cart/') 

@login_required
def add_to_checkout(request):
    cart_item, _ = Cart.objects.get_or_create(user=request.user)
    products = list(cart_item.product.all())
    checkout, _ = Checkout.objects.get_or_create(user=request.user)

    checkout.product.add(*products)
    cart_item.product.remove(*products)
    
    cart_item.save()
    checkout.save()
    messages.success(request, 'products added to checkout')
    return redirect('/checkout/')

@login_required
def place_order(request):
    """Convert checkout to order"""
    checkout = Checkout.objects.filter(user=request.user).first()
    
    if not checkout or checkout.product.count() == 0:
        messages.error(request, 'Your checkout is empty')
        return redirect('/checkout/')
    
    # Create order from checkout
    order = Order.objects.create(
        user=request.user,
        total_amount=checkout.subtotals() or 0,
        status='pending',
        payment_status='pending'
    )
    
    # Add products to order
    order.product.add(*checkout.product.all())
    
    # Clear checkout
    checkout.product.clear()
    
    messages.success(request, f'Order {order.order_number} created successfully!')
    return redirect('order_detail', order_number=order.order_number)

@login_required
def order_detail(request, order_number):
    """Display order details"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = get_base_context(request)
    context['order'] = order
    context['order_products'] = order.product.all()
    return render(request, 'order_detail.html', context)

def remove_from_checkout(request, name):
    checkout, _ = Checkout.objects.get_or_create(user=request.user)
    product = Products.objects.filter(name=name).first()
    checkout.product.remove(product)
    checkout.save()
    messages.success(request, f'{product} removed from checkout')
    return redirect('/checkout/')

def delete_checkout(request):
    checkout, _ = Checkout.objects.get_or_create(user=request.user)
    checkout.delete()
    checkout.save()
    messages.success(request, 'checkout successfully cleared')
    return redirect('/checkout/')


def search_product(request):
    context = get_base_context(request)
    
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['search']
            context["products"] = Products.objects.filter(name__icontains=name)
    else:
        form = SearchForm()

    context['search_form'] = form
    return render(request, 'category-boxed.html', context)


@user_is_superuser_or_staff
def edit_product(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = get_base_context(request)
    
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'{product.name} edited successfully')
            return redirect('/home/')
    else:
        form = ProductEditForm(instance=product)
    
    context['form'] = form
    context['product'] = product
    return render(request, 'product_edit.html', context)

def checkout_test(request):
    return stk_push_success(request)


def samoHomeView(request):
    context = get_base_context(request)
    return render(request, 'index-11.html', context)


@user_is_superuser_or_staff
def listProducts(request):
    context = get_base_context(request)
    context['products'] = Products.objects.all()
    return render(request, 'listproducts.html', context)


@user_is_superuser_or_staff
def disableWoutPic(request):
    products = Products.objects.all()
    for item in products:
        if not item.image:
            item.active = False
            item.save()
    return redirect('/home/')

@user_is_superuser_or_staff
def populateWithStock(request):
    products = Products.objects.all()
    for item in products:
        if item.quantity_in_stock <= 0:
            item.quantity_in_stock = 5
            item.save()
    return redirect('/home/')