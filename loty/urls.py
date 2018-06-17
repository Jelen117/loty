"""loty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from loty2 import views


urlpatterns = [
    path('loty2/', include('loty2.urls')),
    path('admin/', admin.site.urls),
    path('results/', views.results),
    path('results/<str:flight_id>/', views.details),
    path('add_passengers/<str:flight_id>/', views.add_passengers),
    path('show_models', views.show_models),
    url(r'^add_flight_crew', TemplateView.as_view(template_name='static/add_flight_crew.html')),
    url(r'^flight_edit_crew/(?P<pk>[0-9]+)/$', views.FlightEditCrew.as_view()),
    url(r'^login', TemplateView.as_view(template_name='static/login.html')),
    url(r'^flights', views.flights),
    url(r'^crews', views.crews),
    url(r'^2login2', TemplateView.as_view(template_name='loty2/2login2.html'))
]
