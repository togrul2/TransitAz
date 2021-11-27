from django.shortcuts import render
from django.http import JsonResponse
from .models import City, Bus, Train
from user.models import User
import json

# Create your views here.


def getBus(request, pk):
    bus = Bus.objects.get(id=pk)
    return render(request, 'bus.html', context={'bus': bus})


def dashboard(request):
    cities = City.objects.all()
    bus_destinations = {city.name: city.bus_stations.all() for city in cities}
    train_destinations = {city.name: city.train_stations.all() for city in cities}
    return render(request, 'dashboard.html', context={
        'path': 'dashboard',
        'bus_destinations': bus_destinations,
        'train_destinations': train_destinations,
    })


def search_tickets(request):
    cities = City.objects.all()
    bus_destinations = {city.name: city.bus_stations.all() for city in cities}
    train_destinations = {city.name: city.train_stations.all() for city in cities}

    option = request.GET.get('radio-choice')
    results = []
    if option == 'bus-search':
        start_point = request.GET.get('bus-start-station', '')
        arrive_point = request.GET.get('bus-arrive-station', '')
        start_date = request.GET.get('bus-start-date', '')
        arrive_date = request.GET.get('bus-arrive-date', '')

        results = Bus.objects.filter(starting_point__name__contains=start_point,
                                     destination__name__contains=arrive_point,
                                     departures_at__contains=start_date,
                                     arrives_at__contains=arrive_date)

    elif option == 'train-search':
        start_point = request.GET.get('train-start-station', '')
        arrive_point = request.GET.get('train-arrive-station', '')
        start_date = request.GET.get('train-start-date', '')
        arrive_date = request.GET.get('train-arrive-date', '')

        results = Train.objects.filter(starting_point__name__contains=start_point,
                                       destination__name__contains=arrive_point,
                                       departures_at__contains=start_date,
                                       arrives_at__contains=arrive_date)

    return render(request, 'tickets.html', context={'path': 'search-tickets',
                                                    'option': option,
                                                    'results': results,
                                                    'bus_destinations': bus_destinations,
                                                    'train_destinations': train_destinations})


def tickets_cart(request):
    return render(request, 'tickets-cart.html', context={'path': 'tickets-cart'})
