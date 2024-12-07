from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

# TO-DO 1.1: create a settings page, which the dark_mode will be toggled from
# TO-DO 1.2: on every login/logout - take the current value of dark_theme (session variable) and update in db, for persistence
@login_required
def toggle_dark_theme(request):
    if request.method == "POST":
        request.session["dark_theme"] = request.POST.get("dark_theme")
        return JsonResponse({"status": "success", "dark_theme": request.session["dark_theme"]})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def my_profile(request):
    return render(request, 'my_profile.html')

def register_view(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
            except:
                messages.error(request, 'Username already exists.')
                
        else:
            messages.error(request, 'Passwords do not match.')
            
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')