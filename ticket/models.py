from django.db import models
from user.models import User
# Create your models here.


class BusStation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    coords = models.CharField(max_length=100)
    map_x = models.FloatField(null=True, blank=True)
    map_y = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Bus(models.Model):
    class Meta:
        verbose_name_plural = 'busses'

    description = models.CharField(max_length=2000)

    starting_point = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='busses_start')
    destination = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='busses_come')

    capacity = models.IntegerField()
    ticket_price = models.FloatField()

    departures_at = models.DateTimeField()
    arrives_at = models.DateTimeField()

    @property
    def seats_remain(self):
        return self.capacity - self.tickets.all().count()

    def __str__(self):
        return self.description


class BusTicket(models.Model):
    bus = models.ForeignKey(Bus, null=True, on_delete=models.SET_NULL, related_name='tickets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    purchased_at = models.DateTimeField(auto_now_add=True)
