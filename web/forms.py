from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from web.models import Cart, Products, Profile, Order

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'johndoe@gmail.com'}),
        required=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'name':'q'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'name':'q'}))


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search product ...'}),
        required=True
    )

class ProductEditForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',})
    )
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control',})
    )
    sellp = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control',})
    )
    buyp = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control',})
    )
    quantity_in_stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control',})
    )
    order_amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control',})
    )

    class Meta:
        model = Products
        fields = ['name', 'code', 'sellp', 'buyp', 'quantity_in_stock', 'order_amount', 'image', 'active',]
    
class AddToCart(forms.ModelForm):
    order_amount = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1})
    )
    class Meta:
        model = Cart
        fields = ['order_amount',]


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254...'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number']


class UserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ShippingAddressForm(forms.ModelForm):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your full shipping address'}),
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254...'}),
        required=False
    )

    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number']