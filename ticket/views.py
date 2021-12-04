from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import City, Bus, Train, BusTicket, TrainTicket
from django.core.paginator import Paginator
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


def proceedPayment(request):
    data = json.loads(json.loads(request.body))
    if request.user.is_authenticated:
        for item in data:
            for _ in range(int(item['count'])):
                if item['type'] == 'bus-search':
                    bus = Bus.objects.get(id=item['back_id'])
                    ticket = BusTicket(owner=request.user, bus=bus)
                    ticket.save()
                elif item['type'] == 'train-search':
                    train = Train.objects.get(id=item['back_id'])
                    ticket = TrainTicket(owner=request.user, train=train)
                    ticket.save()
    else:
        return JsonResponse("Sign in for making purchase", safe=False, status=403)
    return JsonResponse("Purchase successful", safe=False, status=200)


def paymentDone(request):
    if request.user.is_authenticated:
        return render(request, 'payment-result.html', context={'path': 'tickets-cart', 'success': True})
    else:
        return render(request, 'payment-result.html', context={'path': 'tickets-cart', 'success': False})


def myTickets(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(request.GET.get('next', 'main'))

    # bus_tickets = BusTicket.objects.annotate(Count('bus', distinct=True))
    bus_tickets = BusTicket.objects.filter(owner=user)
    bus_paginator = Paginator(bus_tickets, 5)
    try:
        bus_result = bus_paginator.get_page(request.GET.get('bus_page', 1))
    except:
        bus_result = bus_paginator.get_page(1)

    usable_bus_tickets_count = 0

    for ticket in bus_tickets:
        usable_bus_tickets_count += ticket.is_usable

    train_tickets = TrainTicket.objects.filter(owner=user)
    train_paginator = Paginator(train_tickets, 5)
    try:
        train_result = train_paginator.get_page(request.GET.get('train_page', 1))
    except:
        train_result = train_paginator.get_page(1)

    usable_train_tickets_count = 0
    for ticket in train_tickets:
        usable_train_tickets_count += ticket.is_usable

    total_count = bus_tickets.count() + train_tickets.count()
    train_count = train_tickets.count()
    bus_count = bus_tickets.count()
    return render(request, 'my-tickets.html', context={'bus_tickets': bus_result,
                                                       'usable_bus_tickets_count': usable_bus_tickets_count,
                                                       'train_tickets': train_result,
                                                       'usable_train_tickets_count': usable_train_tickets_count,
                                                       'total_count': total_count,
                                                       'bus_count': bus_count,
                                                       'train_count': train_count
                                                       })
