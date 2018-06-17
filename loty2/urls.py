from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('results/<str:flight_id>/', views.details, name='details'),
    path('add_passengers/<str:flight_id>/', views.add_passengers, name='add_passengers'),
]

