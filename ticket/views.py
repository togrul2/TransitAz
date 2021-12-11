from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import City, Transport, Ticket, Station
from django.core.paginator import Paginator
import json


# Create your views here.


def dashboard(request):
    cities = City.objects.all()
    bus_destinations = {city.name: city.stations.filter(type='Bus') for city in cities}
    train_destinations = {city.name: city.stations.filter(type='Train') for city in cities}
    return render(request, 'dashboard.html', context={
        'path': 'dashboard',
        'bus_destinations': bus_destinations,
        'train_destinations': train_destinations,
    })


def search_tickets(request):
    cities = City.objects.all()
    bus_destinations = {city.name: city.stations.filter(type='Bus') for city in cities}
    train_destinations = {city.name: city.stations.filter(type='Train') for city in cities}

    option = request.GET.get('radio_choice')
    print(request.GET)
    one_or_two_way = request.GET.get('oneortwoway')
    results1, results2 = [], []

    if option == 'bus-search':
        start_point = request.GET.get('bus_start_station', '')
        arrive_point = request.GET.get('bus_arrive_station', '')
        start_date = request.GET.get('bus_start_date', '')
        arrive_date = request.GET.get('bus_arrive_date', '')

        try:
            dates = Transport.objects.values('departures_at')
            results1 = Transport.objects.filter(type='Bus',
                                                starting_point__id=start_point,
                                                destination__id=arrive_point,
                                                departures_at__contains=start_date)
            if one_or_two_way == 'two':
                results2 = Transport.objects.filter(type='Bus',
                                                    starting_point__id=arrive_point,
                                                    destination__id=start_point,
                                                    departures_at__contains=arrive_date)
        except:
            pass

    elif option == 'train-search':
        start_point = request.GET.get('train_start_station', '')
        arrive_point = request.GET.get('train_arrive_station', '')
        start_date = request.GET.get('train_start_date', '')
        arrive_date = request.GET.get('train_arrive_date', '')
        p_count = request.GET.get('train_arrive_date', '')

        try:
            results1 = Transport.objects.filter(type='Train',
                                                starting_point__id=start_point,
                                                destination__id=arrive_point,
                                                departures_at__contains=start_date)
            if one_or_two_way == 'two':
                results2 = Transport.objects.filter(type='Train',
                                                    starting_point__id=arrive_point,
                                                    destination__id=start_point,
                                                    departures_at__contains=arrive_date)
        except:
            pass

        if results1:
            results1 = {i['departures_at']: results1.filter(departures_at=i['departures_at']) for i in
                        results1.values('departures_at')}.items()
        if results2:
            results2 = {i['departures_at']: results2.filter(departures_at=i['departures_at']) for i in
                        results2.values('departures_at')}.items()

    return render(request, 'tickets.html', context={'path': 'search-tickets',
                                                    'option': option,
                                                    'results1': results1,
                                                    'results2': results2,
                                                    'arrive_asked': one_or_two_way == 'two',
                                                    'bus_destinations': bus_destinations,
                                                    'train_destinations': train_destinations,
                                                    'data': request.GET})


def tickets_cart(request):
    return render(request, 'tickets-cart.html', context={'path': 'tickets-cart'})


def proceedPayment(request):
    data = json.loads(json.loads(request.body))
    if request.user.is_authenticated:
        for item in data:
            for seat in item['seats_selected']:
                transport = Transport.objects.get(id=item['id'])
                ticket = Ticket(owner=request.user, transport=transport, is_purchased=True, seat=seat, type=item['type'])
                ticket.save()
                # if item['type'] == 'bus-search':
                #     bus = Bus.objects.get(id=item['back_id'])
                #     ticket = BusTicket(owner=request.user, bus=bus)
                #     ticket.save()
                # elif item['type'] == 'train-search':
                #     train = Train.objects.get(id=item['back_id'])
                #     ticket = TrainTicket(owner=request.user, train=train)
                #     ticket.save()
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
    return render(request, 'my-tickets.html', context={'path': 'my-tickets',
                                                       'bus_tickets': bus_result,
                                                       'usable_bus_tickets_count': usable_bus_tickets_count,
                                                       'train_tickets': train_result,
                                                       'usable_train_tickets_count': usable_train_tickets_count,
                                                       'total_count': total_count,
                                                       'bus_count': bus_count,
                                                       'train_count': train_count
                                                       })


def map_search(request):
    train_stations = TrainStation.objects.all()
    bus_stations = BusStation.objects.all()
    return render(request, 'map.html', context={'path': 'map_search',
                                                'train_stations': train_stations,
                                                'bus_stations': bus_stations,
                                                })
