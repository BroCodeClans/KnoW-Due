from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    path('', views.Home.as_view(), name = 'home'),
    path('reg/', views.RegView.as_view(), name = 'register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
    path('dash/', views.dashView, name = 'dash'),

]
