"""rework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from user import form
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [

    path('',views.home,name='home'),
    path('login/',LoginView.as_view(template_name="user/login.html"),name='login'),
    path('logout',LogoutView.as_view(template_name="user/login.html"),name='logout'),
   path('signup/', views.Register.as_view(), name='signup'),
    path('profile/<int:pk>', views.Profile.as_view(), name='profile')
]
