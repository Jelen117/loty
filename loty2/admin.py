from django.contrib import admin

from .models import *
admin.site.register(Plane)
admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(FlightCrew)
admin.site.register(Captain)
admin.site.register(CrewMember)