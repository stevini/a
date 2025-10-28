from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from web.models import Products

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control',})
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
#    image = forms.CharField(
 #       widget=forms.FileInput(attrs={'class': 'form-control',})
  #  )
#    active = forms.CharField(
 #       widget=forms.CheckboxInput(attrs={'class': 'form-control',})
  #  )

    class Meta:
        model = Products
        fields = ['name', 'code', 'sellp', 'buyp', 'quantity_in_stock', 'order_amount', 'image', 'active',]
    