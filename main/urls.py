from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('stocks/', views.stocks, name='stocks'),
    path('updates/', views.updates, name='updates'),
    path('get_stock_data', views.get_stock_data, name='get_stock_data'),
    path('get_current_stock_price', views.get_current_stock_price, name='get_current_stock_price'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path("toggle-dark-theme/", views.toggle_dark_theme, name="toggle_dark_theme"),
]
