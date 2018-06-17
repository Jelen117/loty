from rest_framework import serializers

from loty2.models import Flight


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    departure_airport = serializers.ReadOnlyField(source='departure_airport.name')
    arrival_airport = serializers.ReadOnlyField(source='arrival_airport.name')
    plane = serializers.ReadOnlyField(source='plane.name')
    date_of_departure = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    date_of_arrival = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    captain_name = serializers.ReadOnlyField(source='flightcrew.captain.name')
    captain_surname = serializers.ReadOnlyField(source='flightcrew.captain.surname')

    class Meta:
        model = Flight
        fields = ('id', 'departure_airport', 'arrival_airport', 'plane', 'date_of_departure', 'date_of_arrival', 'captain_name', 'captain_surname')
