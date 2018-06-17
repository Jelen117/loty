from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, render_to_response
# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.utils import json

from loty2.serializers import FlightSerializer
from .models import Flight, Passenger, BookingForm, Booking, Airport, Plane, FlightCrew, CrewMember
from .forms import DateForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def results(request):
    flights_list = Flight.objects.order_by('-date_of_departure')
    # create a form instance and populate it with data from the request:
    if request.method == 'GET':
        form = DateForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            flights_list2 = flights_list.filter(date_of_departure__date__range=[form.cleaned_data['date_from'], form.cleaned_data['date_to']])
            return render(request, 'loty2/results.html', {'form': form, 'flights_list': flights_list2})
    else:
        form = DateForm()
    return render(request, 'loty2/results.html', {'form': form, 'flights_list': flights_list})


def details(request, flight_id):
    flight = get_object_or_404(Flight, flight_number=flight_id)
    bookings_list = Booking.objects.filter(flight=flight)
    return render(request, 'loty2/details.html', {'flight': flight, 'bookings_list': bookings_list})


@transaction.atomic
def add_passengers(request, flight_id):
    flight = get_object_or_404(Flight, flight_number=flight_id)
    left = flight.plane.seats - flight.tickets_sold
    message2 = "Możesz zakupić maksymalnie " + str(left) + " biletów"
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BookingForm(request.POST)
        new_ticket = form.save(commit=False)
        new_ticket.flight = flight
        # check whether it's valid:
        if form.is_valid() and left >= new_ticket.number_of_tickets and new_ticket.number_of_tickets >= 1:
            form.save()
            flight.tickets_sold += new_ticket.number_of_tickets
            new_ticket.save()
            flight.save()
            message = 'Rezerwacja się dokonała'
            return render_to_response('loty2/new_passenger.html', {'message': message, 'flight_id': flight_id})
        elif left < new_ticket.number_of_tickets:
            message = "Nie możesz zakupić więcej niż " + str(left) + " biletów na wybrany lot"
            return render_to_response('loty2/inproper_data.html', {'message': message, 'flight_id': flight_id})
        else:
            message = "Musisz zakupic co najmniej 1 bilet!";
            return render_to_response('loty2/inproper_data.html', {'message': message, 'flight_id': flight_id})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = BookingForm()
    return render(request, 'loty2/add_passengers.html', {'form': form, 'flight': flight, 'message2': message2})


def new_passenger(request, flight_id):
    return render(request, 'loty2/new_passenger.html', {'flight_id': flight_id})


def show_models(request):
    passengers = Passenger.objects.all()
    flights = Flight.objects.all()
    bookings = Booking.objects.all()
    airports = Airport.objects.all()
    planes = Plane.objects.all()
    flight_crews = FlightCrew.objects.all()
    crew_members = CrewMember.objects.all()
    return render_to_response('loty2/show_models.html', {'passengers': passengers, 'flights': flights, 'bookings': bookings, 'airports': airports, 'planes': planes, 'flight_crews': flight_crews, 'crew_members': crew_members})


def flights(request):
    flights_list = Flight.objects.all()
    flights_list = [z.to_json() for z in flights_list]
    return JsonResponse(flights_list, safe=False)


# class FlightCrewList(generics.ListAPIView):
#     queryset = FlightCrew.objects.all()
#     serializer_class = FlightCrewSerializer

def crews(request):
    crews_list = FlightCrew.objects.all()
    crews_list = [z.to_json() for z in crews_list]
    return JsonResponse(crews_list, safe=False)


class FlightEditCrew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all().order_by('start_time')
    serializer_class = FlightSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        flight_crew = FlightCrew.objects.filter(id=self.request.data['crew_id']).first()
        try:
            instance.flight_crew = flight_crew
            instance.full_clean()
            instance.save()
            response = HttpResponse(json.dumps({'msg': "Przypisano załogę"}),
                                    content_type='application/json')
            response.status_code = 200

            return response
        except ValidationError as e:
            response = HttpResponse(json.dumps({'msg': "Nie można przypisać" + str(e)}),
                                    content_type='application/json')
            response.status_code = 200
            return response
