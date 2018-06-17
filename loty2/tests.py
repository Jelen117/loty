import datetime
from django.test import TestCase, Client
from django.test.selenium import SeleniumTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .models import Flight, Plane, Airport, FlightCrew, Captain

from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC

class Test(TestCase):

    def setUp(self):
        c1 = Captain(name="Abc", surname="Def")
        c2 = Captain(name="Def", surname="123")
        c3 = Captain(name="xD", surname="eeee")
        c1.save()
        c2.save()
        c3.save()
        f1 = FlightCrew(captain=c1)
        f2 = FlightCrew(captain=c2)
        f3 = FlightCrew(captain=c3)
        f1.save()
        f2.save()
        f3.save()
        a1 = Airport(name="Airport1", city="City1")
        a1.save()
        a2 = Airport(name="Airport2", city="City2")
        a2.save()
        p1 = Plane(name="X", seats=25)
        p2 = Plane(name="Y", seats=26)
        p3 = Plane(name="Z", seats=27)
        p1.save()
        p2.save()
        p3.save()
        date1 = datetime.datetime(2000, 1, 1, 14, 35)
        date2 = datetime.datetime(2000, 1, 1, 17, 15)
        date3 = datetime.datetime(2000, 1, 1, 23, 20)
        date4 = date1 + datetime.timedelta(hours=2)
        date5 = date2 + datetime.timedelta(hours=7)
        date6 = date3 + datetime.timedelta(hours=1)
        ff1 = Flight(departure_airport=a1, arrival_airport=a2, plane=p1, flight_number="001", flight_crew=f1, date_of_departure=date1, date_of_arrival=date4)
        ff1.save()
        ff2 = Flight(departure_airport=a2, arrival_airport=a1, plane=p2, flight_number="002", flight_crew=f2, date_of_departure=date2, date_of_arrival=date5)
        ff2.save()
        ff3 = Flight(departure_airport=a1, arrival_airport=a2, plane=p1, flight_number="003", flight_crew=f3, date_of_departure=date3, date_of_arrival=date6)
        ff3.save()

    def test_api_get(self):
        c = Client()
        c.post('login.html', {'username': '123', 'password': 'abc'})


class Test2(SeleniumTestCase):

    def setUp(self):
        c1 = Captain(name="Abc", surname="Def")
        c2 = Captain(name="Def", surname="123")
        c3 = Captain(name="xD", surname="eeee")
        c1.save()
        c2.save()
        c3.save()
        f1 = FlightCrew(captain=c1)
        f2 = FlightCrew(captain=c2)
        f3 = FlightCrew(captain=c3)
        f1.save()
        f2.save()
        f3.save()
        a1 = Airport(name="Airport1", city="City1")
        a1.save()
        a2 = Airport(name="Airport2", city="City2")
        a2.save()
        p1 = Plane(name="X", seats=25)
        p2 = Plane(name="Y", seats=26)
        p3 = Plane(name="Z", seats=27)
        p1.save()
        p2.save()
        p3.save()
        date1 = datetime.datetime(2000, 1, 1, 14, 35)
        date2 = datetime.datetime(2000, 1, 1, 17, 15)
        date3 = datetime.datetime(2000, 1, 1, 23, 20)
        date4 = date1 + datetime.timedelta(hours=2)
        date5 = date2 + datetime.timedelta(hours=7)
        date6 = date3 + datetime.timedelta(hours=1)
        ff1 = Flight(departure_airport=a1, arrival_airport=a2, plane=p1, flight_number="001", flight_crew=f1, date_of_departure=date1, date_of_arrival=date4)
        ff1.save()
        ff2 = Flight(departure_airport=a2, arrival_airport=a1, plane=p2, flight_number="002", flight_crew=f2, date_of_departure=date2, date_of_arrival=date5)
        ff2.save()
        ff3 = Flight(departure_airport=a1, arrival_airport=a2, plane=p1, flight_number="003", flight_crew=f3, date_of_departure=date3, date_of_arrival=date6)
        ff3.save()

        def test_selenium(self):
            driver = webdriver.Chrome()
            driver.get('http://127.0.0.1:8000/login.html')
            driver.find_element_by_name('username').send_keys('abc')
            driver.find_element_by_name('password').send_keys('123')
            driver.find_element_by_id('button').click()
            driver.get('http://127.0.0.1:8000/add_flight_crew.html')
            driver.find_element_by_id('selected_date').send_keys("2000-01-01")
            driver.find_element_by_class_name('get_data').click()
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "change"))
                )
            finally:
                driver.find_element_by_id('change').click()
