from django.urls import path
from . import views

urlpatterns = [
    path('bus/<int:pk>', views.getBus, name='bus'),
    path('', views.search_tickets, name='search-tickets'),
    path('cart/', views.tickets_cart, name='tickets-cart'),

]
