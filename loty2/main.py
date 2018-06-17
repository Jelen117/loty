import datetime

from random import randint

from django.core.serializers import json
from objdict import ObjDict

planes = []
airports = []
flights = []
members = []
captains = []


def generate_planes():
    napis = "ABC"
    liczba = 1234
    global json_string2
    json_string2 = "["
    for i in range(0, 50):
        plane = ObjDict()
        napis2 = napis + str(liczba)
        plane.model = "loty2.plane"
        plane.pk = i + 1
        plane.fields = ObjDict()
        plane.fields.name = napis2
        plane.fields.seats = randint(20, 40)
        planes.append(plane)
        liczba += 1
        json_string2 += plane.dumps()
        if i != 49:
            json_string2 += ","


def generate_airports():
    global json_string
    json_string = "["
    napis = "GHI"
    city = "Warszawa"
    liczba2 = 1
    liczba = 9012
    for i in range(0, 150):
        abc = ObjDict()
        abc.model = "loty2.airport"
        abc.pk = i + 1
        abc.fields = ObjDict()
        abc.fields.name = napis + str(liczba)
        abc.fields.city = city + str(liczba2)
        airports.append(abc)
        liczba += 1
        liczba2 += 1
        json_string += abc.dumps()
        if i != 149:
            json_string += ","


def generate_members():
    napis = "Marek"
    liczba = 1
    global json_string4
    json_string4 = "["
    for i in range(0, 10):
        abc = ObjDict()
        abc.model = "loty2.crewmember"
        abc.pk = i + 1
        abc.fields = ObjDict()
        abc.fields.name = napis + str(liczba)
        members.append(abc)
        liczba += 1
        json_string4 += abc.dumps()
        if i != 9:
            json_string4 += ","

def generate_captains():
    napis = "Jan"
    liczba = 1
    napis2 = "Abcde"
    liczba2 = 1
    global json_string5
    json_string5 = "["
    for i in range (0,10):
        abc = ObjDict()
        abc.model = "loty2.captain"
        abc.pk = i + 1
        abc.fields = ObjDict()
        abc.fields.name = napis + str(liczba)
        abc.fields.surname = napis2 + str(liczba2)
        captains.append(abc)
        liczba+=1
        liczba2+=1
        json_string5 += abc.dumps()
        if i != 9:
            json_string5 += ","


def generate_crews():
    global json_string6
    json_string6 = "["
    for i in range(0, 10):
        flight_crew = '{"model": "loty2.flightcrew", "pk": '
        flight_crew += str(i + 1)
        flight_crew += ', "fields": {"members": ['
        a = randint(0, 9)
        b = randint(0, 9)
        while a == b:
            b = randint(0, 9)
        c = randint(0, 9)
        while a == c or b == c:
            c = randint(0, 9)
        flight_crew += str(a + 1)
        flight_crew += ', '+ str(b + 1)
        flight_crew += ', ' + str(c + 1)
        flight_crew += '], "captain": ' + str(i+1)
        flight_crew += '}}'
        if i != 9:
            flight_crew += ','
        json_string6 += flight_crew


# "captain": {"name": "aahahh", "surname": "ahaheealr"}},

def generate_flights():
    napis = "DEF"
    liczba = 5678
    departure_date = datetime.datetime(2000, 1, 1, 12, 15)
    arrival_date = datetime.datetime(2000, 1, 1, 14, 35)
    global json_string3
    json_string3 = "["
    for i in range(0, 50):
        for j in range(0, 50):
            flight = ObjDict()
            flight.model = "loty2.flight"
            flight.pk = i * 50 + j + 1
            flight.fields = ObjDict()
            flight.fields.flight_number = napis + str(liczba)
            liczba += 1
            flight.fields.plane = j + 1
            miasto1 = randint(0, 149)
            miasto2 = randint(0, 149)
            while miasto2 == miasto1:
                miasto2 = randint(0, 149)
            flight.fields.departure_airport = miasto1 + 1
            flight.fields.arrival_airport = miasto2 + 1
            flight.fields.date_of_departure = departure_date
            flight.fields.date_of_arrival = arrival_date
            flight.fields.flight_crew = j % 10 + 1
            departure_date += datetime.timedelta(hours=6)
            arrival_date += datetime.timedelta(hours=6, minutes=1)
            json_string3 += flight.dumps()
            if i != 49 or j != 49:
                json_string3 += ","


if __name__ == '__main__':
    generate_airports()
    generate_planes()
    generate_flights()
    generate_members()
    generate_captains()
    generate_crews()
    json_string += "]"
    json_string2 += "]"
    json_string3 += "]"
    json_string4 += "]"
    json_string5 += "]"
    json_string6 += "]"
    print(json_string)
    print(json_string4)
    print(json_string5)
    print(json_string6)
    file2write = open("fixtures/fixture.json", 'w')
    file2write.write(json_string)
    file2write.close()
    file2write2 = open("fixtures/fixture2.json", 'w')
    file2write2.write(json_string2)
    file2write2.close()
    file2write3 = open("fixtures/fixture3.json", 'w')
    file2write3.write(json_string3)
    file2write3.close()
    file2write = open("fixtures/fixture4.json", 'w')
    file2write.write(json_string4)
    file2write.close()
    file2write = open("fixtures/fixture5.json", 'w')
    file2write.write(json_string5)
    file2write.close()
    file2write = open("fixtures/fixture6.json", 'w')
    file2write.write(json_string6)
    file2write.close()
