from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_tickets, name='search-tickets'),
    path('cart/', views.tickets_cart, name='tickets-cart'),
    path('proceedtopay/', views.proceedPayment, name='proceed-to-pay'),
    path('my-tickets/', views.myTickets, name='my-tickets'),
    path('map_search/', views.map_search, name='map_search'),
]
