from functools import wraps
from web.forms import CustomLoginForm, CustomUserCreationForm
from web.models import User
from django.contrib.auth import login as trouble, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden   

def speedy_login(func):
    @wraps(func)
    def login_view(request):
        creation_form = CustomUserCreationForm
        login_form = CustomLoginForm()
        result = func(request)
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
                login_form = CustomLoginForm()
                messages.error(request, f"Please correct the errors below.")
                return render(request, 'login.html', {'login_form':login_form,'creation_form':creation_form})
                            
        creation_form = CustomUserCreationForm()
        if "login" in request.POST:
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
            return render(request, 'login.html', {'login_form':login_form,'creation_form':creation_form})
        return result
    return login_view

def user_is_superuser_or_staff(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

