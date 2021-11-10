from django.db import models
from user.models import User
# Create your models here.


class BusStation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    map_x = models.FloatField()
    map_y = models.FloatField()


class Bus(models.Model):
    description = models.CharField(max_length=2000)

    starting_point = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='starting')
    destination = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='destination')

    capacity = models.IntegerField()
    ticket_price = models.FloatField()

    departures_at = models.DateTimeField()
    arrives_at = models.DateTimeField()


class BusTicket(models.Model):
    bus = models.ForeignKey(Bus, null=True, on_delete=models.SET_NULL, related_name='bus')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    purchased_at = models.DateTimeField(auto_now_add=True)
