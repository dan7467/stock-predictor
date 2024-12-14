from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .stock_data_query import StockData
from datetime import datetime, timezone
from .models import CustomUser
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from . import notifications, input_sanitizer

stock_data_handler = StockData()

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def live_crypto(request):
    last_action_timestamp_update(request)
    return render(request, 'live_crypto.html')

def coin_plotter(request):
    last_action_timestamp_update(request)
    return render(request, 'coin_plotter.html')

def home_members(request):
    last_action_timestamp_update(request)
    return render(request, 'home.html')

def about_members(request):
    last_action_timestamp_update(request)
    return render(request, 'about.html')

@login_required
def log_out(request):
    logout(request)
    return redirect('home')

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def get_current_stock_price(request):
    body = json.loads(request.body)
    ticker = body.get('stock_symbol')
    if ticker and input_sanitizer.is_sanitized_stock_symbol(ticker):
        res = stock_data_handler.fetch_current_day_stock_info(json.loads(request.body).get('stock_symbol'))
        return JsonResponse({"status": "success", "data": res.to_json()})
    return JsonResponse({"status": "error", "message": "Invalid input."})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def get_company_info(request):
    body = json.loads(request.body)
    ticker = body.get('stock_symbol')
    if ticker and input_sanitizer.is_sanitized_stock_symbol(ticker):
        return JsonResponse({"status": "success", "data": stock_data_handler.fetch_company_info(ticker)})
    return JsonResponse({"status": "error", "message": "No Symbol was entered."}, status=400)

@login_required
def last_action_timestamp_update(request):
    profile = CustomUser.objects.get(username=request.user.username)
    new_updates = notifications.check_updates(request, profile, stock_data_handler)
    if len(new_updates) > 0:  # means new_updates is a list where update == ["%H:%M:%S, %d.%m.%y", subscribed_update, directive_dir, directive_val]
        for update in new_updates:
            notifications.add_user_stock_notification(request, profile, update)
            del profile.user_updates[update[1]]
            profile.save()
    profile.last_action_datetime_utc = datetime.now(timezone.utc).strftime("%H:%M:%S, %d.%m.%y")
    profile.save()
    

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if input_sanitizer.are_sanitized_strings([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_members')
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def my_profile(request):
    last_action_timestamp_update(request)
    if request.method == 'POST':
        if request.POST.get('_method', False) == 'DELETE':
            stock_symbol = request.POST.get('_stock_sym', False)
            if input_sanitizer.is_sanitized_stock_symbol(stock_symbol):
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

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def get_stock_data(request):
    body = json.loads(request.body)
    ticker = body.get('stock_symbol')
    start_date = body.get('from_date')
    end_date = body.get('to_date')
    if input_sanitizer.is_sanitized_stock_symbol(ticker):
        if start_date == 'ALL' and ticker:
            return JsonResponse({"status": "success", "data": stock_data_handler.fetch_all_stock_data(ticker).to_json()})
        if start_date == end_date == datetime.now().strftime('%Y-%m-%d'):
            return JsonResponse({"status": "success", "data": stock_data_handler.fetch_current_day_stock_info(ticker).to_json()})
        dates_valid = datetime.strptime(start_date, '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d')
        if ticker and start_date and end_date and dates_valid:
            return JsonResponse({"status": "success", "data": stock_data_handler.fetch_data(ticker, start_date, end_date).to_json()})
    return JsonResponse({"status": "error", "message": "Invalid input or request method"}, status=400)

@login_required
def updates(request):
    last_action_timestamp_update(request)
    profile = CustomUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_sym', False)     
        directive = request.POST.get('price_direction', False)
        directive_value = request.POST.get('bound_val', False)  
        if input_sanitizer.are_sanitized_strings([directive, directive_value]) and input_sanitizer.is_sanitized_stock_symbol(stock_symbol): 
            # create a new subscription:
            if request.POST.get('_method') == 'PATCH': 
                timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S, %d.%m.%y")
                if stock_symbol and directive and directive_value and stock_symbol not in profile.user_updates and stock_data_handler.check_if_symbol_exists(stock_symbol):
                    try:
                        profile.user_updates[stock_symbol] = [timestamp, directive, directive_value]
                        profile.save()
                        return render(request, 'updates.html', {'my_stocks': profile.my_stocks, 'my_updates': profile.user_updates})
                    except Exception as e:
                        return JsonResponse({f"status": "error", "message": "Error occurred while creating subscription"})
                return render(request, 'updates.html', {'my_stocks': profile.my_stocks, 'my_updates': profile.user_updates, 'error_msg': f'Error: Symbol {stock_symbol} does not exist.'})
            # delete existing subscription:
            elif request.POST.get('_method') == 'DELETE':
                if stock_symbol and directive and directive_value and stock_symbol in profile.user_updates:
                    try:
                        del profile.user_updates[stock_symbol]
                        profile.save()
                        return render(request, 'updates.html', {'my_stocks': profile.my_stocks, 'my_updates': profile.user_updates})
                    except Exception as e:
                        return JsonResponse({f"status": "error", "message": "Error occurred while deleting subscription"})
                return JsonResponse({"status": "error", "message": "Error: Stock subscription doesn't exist"})
            # delete existing notification:
            elif request.POST.get('_method') == 'DELETE_NOTIFICATION':
                if request.POST.get('del_notification_id', False):
                    try:
                        profile.user_notifications.pop(int(request.POST.get('del_notification_id')) - 1)
                        profile.save()
                        return redirect('updates')
                    except Exception as e:
                        return JsonResponse({f"status": "error", "message": "Error occurred while deleting notification"})
                return JsonResponse({"status": "error", "message": "Error: notification doesn't exist"})
            return JsonResponse({"status": "error", "message": "Error: Wrong method (should be PATCH or DELETE)"})
        return render(request, 'updates.html', {'my_stocks': profile.my_stocks, 'my_updates': profile.user_updates, 'error_msg': f'Error: Invalid input.'})
    if len(profile.user_updates) == 0:
        return render(request, 'updates.html', {'my_stocks': profile.my_stocks})
    return render(request, 'updates.html', {'my_stocks': profile.my_stocks, 'my_updates': profile.user_updates})

@login_required
@csrf_exempt
@require_http_methods(["POST", "GET"])
def stocks(request):
    last_action_timestamp_update(request)
    profile = CustomUser.objects.get(username=request.user.username)   
    if request.method == 'POST':
        if request.POST.get('_method') == 'PATCH':
            stock_symbol = request.POST.get('_symbol', False)      
            if input_sanitizer.is_sanitized_stock_symbol(stock_symbol):   
                if stock_symbol and stock_symbol not in profile.my_stocks and stock_data_handler.check_if_symbol_exists(stock_symbol):
                    try:
                        profile.my_stocks.append(stock_symbol)
                        profile.save()
                        messages.success(request, f"Stock {stock_symbol} added to 'My Stocks'!")
                    except Exception as e:
                        messages.error(request, f"Could not update stock: {e}")
                else:
                    messages.error(request, 'No stock symbol was entered!')
                return render(request, 'stocks.html', {'chosen_stock_name': stock_symbol, 'my_stocks': profile.my_stocks})  # Re-render the same page
    return render(request, 'stocks.html', {'my_stocks': profile.my_stocks})


def register(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        
        if input_sanitizer.are_sanitized_strings([username, password, confirm_password, email]):
        
            if password == confirm_password:
                try:
                    user = CustomUser.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        my_stocks=[],
                        last_action_datetime_utc=datetime.now().replace(tzinfo=timezone.utc).strftime("%H:%M:%S, %d.%m.%y")
                    )
                    user.save()
                    messages.success(request, 'Registration successful! Please log in.')
                    return redirect('login')
                except:
                    messages.error(request, 'Username already exists.')
                    
            else:
                messages.error(request, 'Passwords do not match.')
            
    return render(request, 'register.html')

