from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path("toggle-dark-theme/", views.toggle_dark_theme, name="toggle_dark_theme"),
]
