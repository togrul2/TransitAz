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
from django.urls import path, include
# noinspection PyCompatibility
from user import views as user_views
from ticket import views as ticket_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth views
    path('login/', user_views.loginUser, name='login'),
    path('register/', user_views.registerUser, name='register'),
    path('logout/', user_views.logoutUser, name='logout'),
    path('', ticket_views.main, name='main'),
    path('activate-user/<str:uidb64>/<str:token>', user_views.activate_user, name='activate'),
    path('activation-request', user_views.activation_request, name='activation_request'),
    # Reset Password views
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="auth/reset/reset_password_request.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="auth/reset/reset_password_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="auth/reset/reset_password.html"),
         name='password_reset_confirm'),
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="auth/reset/reset_password_complete.html"),
         name='password_reset_complete'),
    # Ticket views
    path('dashboard/', ticket_views.dashboard, name='dashboard'),
    path('about_us/', ticket_views.about_us, name='about_us'),
    path('rules/', ticket_views.rules, name='rules'),
    path('ticket/', include('ticket.urls')),
    # User views
    path('user/', include('user.urls')),
]
