from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer
from django.contrib.auth import logout as auth_logout  # Rename the imported function


def show_accounts(request):
    context = {}
    if request.method == 'POST' and 'register' in request.POST:
        context['register'] = True
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                raise ValueError("Username already exists")
            if User.objects.filter(email=email).exists():
                raise ValueError("Email already exists")
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create customer profile
            customer = Customer.objects.create(
                name = username,
                user=user,
                phone=phone,
                address=address
            )
            success_message = "Registration successful. You can now log in."
            messages.success(request, success_message)

        except ValueError as e:
            messages.error(request, str(e))  # Display specific error message
        except Exception as e:
            messages.error(request, "An error occurred during registration")
        
    # Login the user
    if 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'account.html', context)

def logout(request):
    auth_logout(request)  # Call the renamed function
    return redirect('index')