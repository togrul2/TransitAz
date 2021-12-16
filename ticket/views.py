from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import City, Transport, Ticket, Station
from django.core.paginator import Paginator
import json


# Create your views here.

def main(request):
    return render(request, 'main.html')


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
    # bus_destinations = Station.objects.filter(type='Bus')
    # train_destinations = Station.objects.filter(type='Train')

    bus_destinations = {city.name: city.stations.filter(type='Bus') for city in cities}
    train_destinations = {city.name: city.stations.filter(type='Train') for city in cities}

    option = request.GET.get('radio_choice')
    one_or_two_way = request.GET.get('oneortwoway')
    results1, results2 = [], []

    if option == 'bus-search':
        start_point = request.GET.get('bus_start_station', '')
        arrive_point = request.GET.get('bus_arrive_station', '')
        start_date = request.GET.get('bus_start_date', '')
        arrive_date = request.GET.get('bus_arrive_date', '')

        try:
            results1 = Transport.objects.filter(type='Bus',
                                                starting_point__description=start_point,
                                                destination__description=arrive_point,
                                                departures_at__contains=start_date)
            if one_or_two_way == 'two':
                results2 = Transport.objects.filter(type='Bus',
                                                    starting_point__description=arrive_point,
                                                    destination__description=start_point,
                                                    departures_at__contains=arrive_date)
        except:
            pass

    elif option == 'train-search':
        start_point = request.GET.get('train_start_station', '')
        arrive_point = request.GET.get('train_arrive_station', '')
        start_date = request.GET.get('train_start_date', '')
        arrive_date = request.GET.get('train_arrive_date', '')

        try:
            results1 = Transport.objects.filter(type='Train',
                                                starting_point__description=start_point,
                                                destination__description=arrive_point,
                                                departures_at__contains=start_date)
            if one_or_two_way == 'two':
                results2 = Transport.objects.filter(type='Train',
                                                    starting_point__description=arrive_point,
                                                    destination__description=start_point,
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
                                                    'bus_destinations': bus_destinations,
                                                    'train_destinations': train_destinations})


def tickets_cart(request):
    return render(request, 'tickets-cart.html', context={'path': 'tickets-cart'})


def proceedPayment(request):
    data = json.loads(json.loads(request.body))
    if request.user.is_authenticated:
        for item in data:
            for seat in item['seats_selected']:
                transport = Transport.objects.get(id=item['id'])
                ticket = Ticket(owner=request.user, transport=transport, is_purchased=True, seat=seat,
                                type=item['type'])
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

    filter_opt = request.GET.get('filter', '')
    total = Ticket.objects.filter(owner=request.user).count()
    train_total = Ticket.objects.filter(owner=request.user, transport__type='Train').count()
    bus_total = Ticket.objects.filter(owner=request.user, transport__type='Bus').count()
    usable_tickets = len(list(filter(lambda obj: obj.is_usable, list(Ticket.objects.filter(owner=request.user)))))
    usable_train_tickets = len(list(
        filter(lambda obj: obj.is_usable, list(Ticket.objects.filter(owner=request.user, transport__type='Train')))))
    usable_bus_tickets = len(
        list(filter(lambda obj: obj.is_usable, list(Ticket.objects.filter(owner=request.user, transport__type='Bus')))))

    if filter_opt == 'active':
        tickets = list(filter(lambda obj: obj.is_usable, list(Ticket.objects.filter(owner=request.user))))
    elif filter_opt == 'bus_only':
        tickets = Ticket.objects.filter(owner=request.user, transport__type='Bus')
    elif filter_opt == 'train_only':
        tickets = Ticket.objects.filter(owner=request.user, transport__type='Train')
    else:
        tickets = Ticket.objects.filter(owner=request.user)

    paginator = Paginator(tickets, 10)

    try:
        result = paginator.get_page(request.GET.get('page', 1))
    except:
        result = paginator.get_page(1)

    return render(request, 'my-tickets.html', context={'path': 'my-tickets',
                                                       'tickets': result,
                                                       'total': total,
                                                       'train_total': train_total,
                                                       'bus_total': bus_total,
                                                       'usable_tickets': usable_tickets,
                                                       'usable_train_tickets': usable_train_tickets,
                                                       'usable_bus_tickets': usable_bus_tickets})


def map_search(request):
    train_stations = Station.objects.filter(type='Train')
    bus_stations = Station.objects.filter(type='Bus')
    return render(request, 'map.html', context={'path': 'map_search',
                                                'train_stations': train_stations,
                                                'bus_stations': bus_stations})
