from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_tickets, name='search-tickets'),
    path('cart/', views.tickets_cart, name='tickets-cart'),
    path('proceedtopay/', views.proceedPayment, name='proceed-to-pay'),
    path('my-tickets/', views.myTickets, name='my_tickets'),
    path('map-search/', views.map_search, name='map_search'),
    path('return-tickets/', views.tickets_for_return, name='return_tickets'),
    path('return-ticket/<int:pk>', views.return_ticket, name='return_ticket'),
]
