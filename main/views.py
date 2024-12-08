from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .plotter import Plotter
from .stock_data_query import StockData
from datetime import datetime, timedelta

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
def stocks(request):
    if request.method == 'POST':
        
        # init facade:
        p = Plotter()
        s = StockData()
        
        ticker = request.POST.get('stock_sym', False)
        start_date = request.POST.get('date_start', False)
        end_date = request.POST.get('date_end', False)
        
        # validate dates
        dates_valid = datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d')
        
        if ticker and start_date and end_date and dates_valid:
            
            x_axis_property = "Date"
            y_axis_property = "Close"
            
            data = s.fetch_data(ticker, start_date, end_date)
            graph = p.plot(data, x_axis_property, y_axis_property, stock_name=ticker, includes_prediction=True, dark_mode=request.session["dark_theme"])
            
            return render(request, 'stocks.html', {'graph': graph, 'stock_name': ticker})
        
    # # TO-DO: save stock to My Stocks:
    # elif request.method == 'PATCH':
    #     stock_symbol = request.POST.get('stock_sym', False)
        
    #     if stock_symbol:
    #         try:
    #             user = User.objects.create_user(username=username, password=password, email=email)
    #             user.save()
    #             messages.success(request, 'Registration successful! Please log in.')
    #             return redirect('login')
    #         except:
    #             messages.error(request, 'Username already exists.')
                
    #     else:
    #         messages.error(request, 'No stock symbol was entered!')
        
    return render(request, 'stocks.html')


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