from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .stock_data_query import StockData
from datetime import datetime, timedelta
from .models import CustomUser
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

stock_data_handler = StockData()

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
def updates(request):
    profile = CustomUser.objects.get(username=request.user.username)
    return render(request, 'updates.html', {'my_stocks': profile.my_stocks})

@login_required
@csrf_exempt
def get_current_stock_price(request):
    res = stock_data_handler.fetch_current_stock_info(json.loads(request.body).get('stock_symbol'))
    print('\n\n\nres = ', res,'\n\n\n')
    return JsonResponse({"status": "success", "data": res.to_json()})

@login_required
@csrf_exempt
@require_http_methods(["POST"])  # TO-DO: change to a get request.. this should not be a POST
def get_stock_data(request):
    body = json.loads(request.body)
    print(f'\n\n\nREQUEST = {body.get('stock_symbol')}\n\n\n')
    ticker = body.get('stock_symbol')
    start_date = body.get('from_date')
    end_date = body.get('to_date')
    dates_valid = datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d')
        
    if ticker and start_date and end_date and dates_valid:
            
        return JsonResponse({"status": "success", "data": stock_data_handler.fetch_data(ticker, start_date, end_date).to_json()})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@login_required
def stocks(request):
    profile = CustomUser.objects.get(username=request.user.username)
    return render(request, 'stocks.html', {'my_stocks': profile.my_stocks})

@login_required
def my_profile(request):
    if request.method == 'POST':
        if request.POST.get('_method', False) == 'DELETE':
            stock_symbol = request.POST.get('_stock_sym', False)
            if stock_symbol:
                profile = CustomUser.objects.get(username=request.user.username)
                try:
                    profile.my_stocks.remove(stock_symbol)
                    profile.save()
                    messages.success(request, f"Stock {stock_symbol} removed from 'My Stocks'")
                    return render(request, 'my_profile.html', {'deleted': stock_symbol})
                except Exception as e:
                    messages.error(request, f"Could not update stock: {e}")
    return render(request, 'my_profile.html')

def register_view(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        
        if password == confirm_password:
            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    my_stocks=[]
                )
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