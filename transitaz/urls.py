"""transitaz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the utils() function: from django.urls import utils, path
    2. Add a URL to urlpatterns:  path('blog/', utils('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth views
    path('login/', user_views.loginUser, name='login'),
    path('register/', user_views.registerUser, name='register'),
    path('logout/', user_views.logoutUser, name='logout'),
    path('', user_views.main, name='main'),
    path('activate-user/<str:uidb64>/<str:token>', user_views.activate_user, name='activate')
    # Ticket views
]
