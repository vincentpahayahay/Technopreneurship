from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
import json
from cart.cart import Cart

def  update_info(request):
    categ = Category.objects.all()
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, ("Your Info Has Been Updated!!"))
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'categ':categ, 'shipping_form':shipping_form})
    else:
        messages.success(request, ("You Must Be Logged In To Access That Page!!"))
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()  # Save the new password
                update_session_auth_hash(request, user)  # Prevents logout after password change
                messages.success(request, "Your password has been updated successfully!")
                return redirect('home')  # Redirect to a success page
            else:
                messages.error(request, "Please correct the errors below.")  # Display errors if form is invalid
        else:
            form = ChangePasswordForm(request.user)
        
        return render(request, 'update_password.html', {'form': form})
    
    else:
        messages.error(request, "You must be logged in to access that page.")
        return redirect('home')

'''
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            pass
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, ("You Must Be Logged In To Access That Page!!"))
        return redirect('home')
'''
    

def update_user(request):
    categ = Category.objects.all()
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, ("User Has Been Updated!!"))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'categ':categ})
    else:
        messages.success(request, ("You Must Be Logged In To Access That Page!!"))
        return redirect('home')


def category(request,foo):
    
    
    try:
        category_name = foo.replace('-',' ')
        categ = Category.objects.all()
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category, 'categ':categ})
    except:
        messages.success(request, ("That Category does not exist..."))
        return redirect('home')

def product(request, pk):
    categ = Category.objects.all()
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product, 'categ':categ})

def home(request):
    products = Product.objects.all()
    categ = Category.objects.all()
    return render(request, 'home.html', {'products':products, 'categ': categ})

def about(request):
    categ = Category.objects.all()
    return render(request, 'about.html', {'categ': categ})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user =authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            
            messages.success(request, ("You have been logged in..."))
            return redirect('home')
        else:
            messages.success(request, ("There was an Error, Please try again.. :("))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out... Thanks for stopping by..."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    categ = Category.objects.all()
    if request.method=="POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']

            user=authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registered - Please Fill Out To Complete Your Profile"))
            return redirect('update_info')
        else:
            messages.success(request, ("Oops... There was a problem, Please try again :("))
            return redirect('register')
    else:        
        return render(request, 'register.html', {'form':form, 'categ': categ})

