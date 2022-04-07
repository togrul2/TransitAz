import datetime
import pytz
from django.test import TestCase
from ticket.models import City, Transport, Station, Ticket
from user.models import User


class TestTransportModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='john',
            last_name='doe',
            email='johndoe@example.com',
            username='johndoe',
            is_verified=True
        )
        self.user.set_password('password123')
        self.start_city = City.objects.create(name='Baku')
        self.destination_city = City.objects.create(name='Ganja')
        self.train_start_station = Station.objects.create(
            name='Baku central station',
            type='Train',
            description='',
            region='Baku',
            city=self.start_city
        )
        self.train_destination_station = Station.objects.create(
            name='Ganja central station',
            type='Train',
            description='',
            region='Ganja',
            city=self.destination_city
        )
        self.transport = Transport.objects.create(
            description='',
            type='Train',
            starting_point=self.train_start_station,
            destination=self.train_destination_station,
            capacity=500,
            units=5,
            price=2,
            low_cost_price=1.5,
            business_price=3.5,
            discount=0.15,
            departures_at=datetime.datetime(2022, 5, 25, 14, tzinfo=pytz.UTC),
            arrives_at=datetime.datetime(2022, 5, 25, 17, tzinfo=pytz.UTC),
            has_seats_for_disabled=True,
            has_wifi=False,
            has_sockets=True,
            has_air_conditioning=True,
            has_multimedia=False,
            has_free_snacks=False,
        )
        self.tickets = []
        for i in range(1, 6):
            ticket = Ticket.objects.create(
                type='Standart',
                transport=self.transport,
                owner=self.user,
                seat=i,
                is_purchased=True,
                purchased_at=datetime.datetime(2022, 4, 7, 15, 32, 24, tzinfo=pytz.UTC)
            )
            self.tickets.append(ticket)

    def test_price_with_discount(self):
        self.assertEquals(self.transport.price_with_discount, 2 * 0.15)

    def test_available_tickets(self):
        self.assertListEqual(self.transport.available_tickets, [i for i in range(6, self.transport.capacity + 1)])

    def test_seats_remain(self):
        self.assertEquals(self.transport.seats_remain, 495)
