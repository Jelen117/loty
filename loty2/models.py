import datetime
from django.db import models
from django.forms import ModelForm, forms

from django.core.exceptions import ValidationError


class Plane(models.Model):
    name = models.CharField(max_length=20)
    seats = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "seats": self.seats
        }


class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "city": self.city
        }


class Passenger(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)

    def __str__(self):
        return self.name + " " + self.surname


class Employee(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)

    class Meta:
        abstract = True


class CrewMember(Employee):
    name = models.CharField(max_length=15)

    def to_json(self):
        return {
            "name": self.name
        }


class Captain(Employee):
    name = models.CharField(unique=True, max_length=15)
    surname = models.CharField(unique=True, max_length=15)

    def to_json(self):
        return {
            "name": self.name,
            "surname": self.surname
        }


class FlightCrew(models.Model):
    members = models.ManyToManyField(CrewMember, default="")
    captain = models.OneToOneField(Captain, on_delete=models.CASCADE)

    def to_json(self):
        return {
            "id": self.id,
            "members": [x.to_json() for x in self.members.all()],
            "captain": self.captain.to_json()
        }

    def __str__(self):
        return self.captain.name + ' ' + self.captain.surname

    # def clean(self):
    #     flight_crews = FlightCrew.objects.all().filter(captain=self.captain).exclude(id=self.id)
    #     if self.date_of_arrival - self.date_of_departure < datetime.timedelta(minutes=30):
    #         raise ValidationError('flight needs to last at least half an hour')
    #     if flight.len >= 4:
    #         raise ValidationError('one plane can do maximally 4 flights a day')


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    tickets_sold = models.IntegerField(default=0)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure", null=True)
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrival", null=True)
    date_of_departure = models.DateTimeField()
    date_of_arrival = models.DateTimeField()
    flight_crew = models.ForeignKey(FlightCrew, on_delete=models.CASCADE, related_name="crew", null=True)

    def __str__(self):
        return self.flight_number

    def to_json(self):
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "plane": self.plane.to_json(),
            "tickets_sold": self.tickets_sold,
            "departure_airport": self.departure_airport.to_json(),
            "arrival_airport": self.arrival_airport.to_json(),
            "date_of_departure": self.date_of_departure,
            "date_of_arrival": self.date_of_arrival,
            "flight_crew": self.flight_crew.to_json()
        }

    def clean(self):
        flights = Flight.objects.all().filter(plane=self.plane).filter(
            date_of_departure__year=self.date_of_departure.year).filter(
            date_of_departure__month=self.date_of_departure.month).filter(
            date_of_departure__day=self.date_of_departure.day);
        if len(flights) >= 4:
            raise ValidationError('one plane can do maximally 4 flights a day')
        if self.date_of_arrival - self.date_of_departure < datetime.timedelta(minutes=30):
            raise ValidationError('flight needs to last at least half an hour')
        flights = Flight.objects.all().filter(plane=self.plane).filter(
            date_of_arrival__gt=self.date_of_departure).filter(date_of_departure__lt=self.date_of_departure).exclude(
            id=self.id)
        if len(flights) >= 1:
            raise ValidationError('one plane can serve only one flight at the same time')
        flights = Flight.objects.all().filter(plane=self.plane).filter(
            date_of_departure__lt=self.date_of_arrival).filter(date_of_arrival__gt=self.date_of_arrival).exclude(
            id=self.id)
        if len(flights) >= 1:
            raise ValidationError('one plane can serve only one flight at the same time')
        flights = Flight.objects.all().filter(flight_crew=self.flight_crew)
        flights = flights.filter(
            date_of_arrival__gt=self.date_of_departure).exclude(id=self.id).filter(date_of_departure__lt=self.date_of_departure)
        if len(flights) >= 1:
            raise ValidationError('one flight crew can serve only one flight at the same time')
        flights = Flight.objects.all().filter(flight_crew=self.flight_crew).filter(
            date_of_arrival__gt=self.date_of_departure).filter(date_of_departure__lt=self.date_of_departure)
        if len(flights) >= 1:
            raise ValidationError('one flight crew can serve only one flight at the same time')


class PassengerForm(ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'surname']


class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="passenger", null=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="flight", null=True)
    number_of_tickets = models.IntegerField(default=0)


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger', 'number_of_tickets']
        labels = {
            "passenger": "Pasażer",
            "number_of_tickets": "Bilety"
        }
