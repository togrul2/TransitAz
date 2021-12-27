import datetime

from django.utils import timezone
from django.db import models
from user.models import User
# Create your models here.


class City(models.Model):
    class Meta:
        verbose_name_plural = 'cities'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Station(models.Model):
    TYPES = (
        ('Bus', 'Bus'),
        ('Train', 'Train')
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPES, default='Bus')
    description = models.CharField(max_length=2000)
    region = models.CharField(max_length=50)
    coords = models.CharField(max_length=1000, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='stations')
    map_x = models.FloatField(null=True, blank=True)
    map_y = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.type}: {self.description}'


class Transport(models.Model):
    TYPES = (
        ('Bus', 'Bus'),
        ('Train', 'Train')
    )

    description = models.CharField(max_length=2000)
    type = models.CharField(max_length=10, choices=TYPES, default='Bus')
    starting_point = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='start')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrive')
    capacity = models.IntegerField()
    units = models.IntegerField(default=1)

    price = models.FloatField(default=1)
    low_cost_price = models.FloatField(default=1)
    business_price = models.FloatField(default=1)
    discount = models.FloatField(default=0)

    departures_at = models.DateTimeField(null=True, blank=True)
    arrives_at = models.DateTimeField(null=True, blank=True)

    has_seats_for_disabled = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_sockets = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    has_multimedia = models.BooleanField(default=False)
    has_free_snacks = models.BooleanField(default=False)

    @property
    def available_tickets(self):
        return [seat for seat in range(1, self.capacity + 1) if not self.tickets.filter(seat=seat).exists()]

    @property
    def seats_remain(self):
        return self.capacity - self.tickets.all().count()

    def __str__(self):
        return f'{self.type}: {self.description}'


class Ticket(models.Model):
    class Meta:
        ordering = '-purchased_at',

    ticket_types = (
        ('Standart', 'Standart'),
        ('Ekonom', 'Ekonom'),
        ('Biznes', 'Biznes'),
    )

    type = models.CharField(max_length=100, choices=ticket_types, default='Standart')
    transport = models.ForeignKey(Transport, null=True, on_delete=models.SET_NULL, related_name='tickets')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    seat = models.IntegerField(default=1)
    is_purchased = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now_add=True)
    # food_option = models.BooleanField(default=False)

    def was_purchased(self):
        return self.objects.filter(bus=self.transport, seat=self.seat).exists()

    def __str__(self):
        return f'{self.type}: {self.owner} - {self.transport}'

    @property
    def is_usable(self):
        return self.transport.departures_at > timezone.now()

    @property
    def is_returnable(self):
        return self.transport.departures_at - datetime.timedelta(days=1) > timezone.now()
