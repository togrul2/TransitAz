from django.db import models
from user.models import User
# Create your models here.


class City(models.Model):
    class Meta:
        verbose_name_plural = 'cities'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BusStation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    region = models.CharField(max_length=50)
    coords = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='bus_stations')
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
        return self.capacity - self.bus_tickets.all().count()

    def __str__(self):
        return self.description


class BusTicket(models.Model):
    bus = models.ForeignKey(Bus, null=True, on_delete=models.SET_NULL, related_name='bus_tickets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bus_tickets')
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner}: {self.bus} at {self.purchased_at}'


class TrainStation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    region = models.CharField(max_length=50)
    coords = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='train_stations')
    map_x = models.FloatField(null=True, blank=True)
    map_y = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    description = models.CharField(max_length=2000)
    starting_point = models.ForeignKey(TrainStation, on_delete=models.CASCADE, related_name='trains_start')
    destination = models.ForeignKey(TrainStation, on_delete=models.CASCADE, related_name='trains_come')
    capacity = models.IntegerField()
    ticket_price = models.FloatField()
    departures_at = models.DateTimeField()
    arrives_at = models.DateTimeField()

    @property
    def seats_remain(self):
        return self.capacity - self.train_tickets.all().count()

    def __str__(self):
        return self.description


class TrainTicket(models.Model):
    train = models.ForeignKey(Train, null=True, on_delete=models.SET_NULL, related_name='train_tickets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='train_tickets')
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner}: {self.train} at {self.purchased_at}'
