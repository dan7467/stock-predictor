from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('home_members/', views.home_members, name='home_members'),
    path('about_members/', views.about_members, name='about_members'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_overview/', views.dashboard_overview, name='dashboard_overview'),
    path('stocks/', views.stocks, name='stocks'),
    path('stocks_home/', views.stocks_home, name='stocks_home'),
    path('updates/', views.updates, name='updates'),
    path('stock_exists', views.stock_exists, name='stock_exists'),
    path('get_stock_data', views.get_stock_data, name='get_stock_data'),
    path('get_crypto_coin_list', views.get_crypto_coin_list, name='get_crypto_coin_list'),
    path('get_company_info', views.get_company_info, name='get_company_info'),
    path('get_current_stock_price', views.get_current_stock_price, name='get_current_stock_price'),
    path('register/', views.register, name='register'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('crypto_live/', views.crypto_live, name='crypto_live'),
    path('crypto_live_plotter/', views.crypto_live_plotter, name='crypto_live_plotter'),
]
