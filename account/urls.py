from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AccountView, name='account'),
    path('login/', views.LogInView, name='login'),
    path('logout/', views.LogOutView, name='logout'),
    path('register/', views.RegisterView, name='register'),
]