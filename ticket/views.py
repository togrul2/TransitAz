from django.shortcuts import render
from .models import Bus
# Create your views here.


def getBus(request, pk):
    bus = Bus.objects.get(id=pk)
    return render(request, 'bus.html', context={'bus': bus})
