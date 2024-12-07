from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .plotter import Plotter
from .stock_data_query import StockData
from datetime import datetime, timedelta
from .models import CustomUser

stock_data_handler = StockData()
graph_plot_handler = Plotter()

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
    profile = CustomUser.objects.get(username=request.user.username)   
    if request.method == 'POST':
        # if this is a PATCH simulation - it is merely a stock saving to My Stocks
        if request.POST.get('_method') == 'PATCH':
            stock_symbol = request.POST.get('_symbol', False)         
            if stock_symbol and stock_symbol not in profile.my_stocks and stock_data_handler.check_if_symbol_exists(stock_symbol):
                try:
                    profile.my_stocks.append(stock_symbol)
                    profile.save()
                    messages.success(request, f"Stock {stock_symbol} added to 'My Stocks'!")
                except Exception as e:
                    messages.error(request, f"Could not update stock: {e}")
            else:
                messages.error(request, 'No stock symbol was entered!')
            return render(request, 'stocks.html', {'stock_name': stock_symbol, 'my_stocks': profile.my_stocks})  # Re-render the same page
        
        # Plot stock data based on user inputs:
        
        # TO-DO: implement cache such that if range was thinned down (new_date_start >= old _date_start and new_date_end <= old_date_end),
        #           then we use the already retrieved info from yf instead of re-calling it
        ticker = request.POST.get('stock_sym', False)
        start_date = request.POST.get('date_start', False)
        end_date = request.POST.get('date_end', False)
        
        # validate dates
        dates_valid = datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d')
        
        if ticker and start_date and end_date and dates_valid:
            
            x_axis_property = "Date"
            y_axis_property = "Close"
            
            data = stock_data_handler.fetch_data(ticker, start_date, end_date)
            graph = graph_plot_handler.plot(data, x_axis_property, y_axis_property, stock_name=ticker, includes_prediction=True, dark_mode=request.session["dark_theme"])
            
            return render(request, 'stocks.html', {'graph': graph, 'stock_name': ticker, 'my_stocks': profile.my_stocks})
        
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