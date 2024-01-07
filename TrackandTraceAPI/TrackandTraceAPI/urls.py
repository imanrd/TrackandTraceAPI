"""
URL configuration for TrackandTraceAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from ShipTrackWeather.views import WeatherShipmentView, home_page
from ShipTrackWeather.swagger import urlpatterns as swagger_urls
from django.urls import path


urlpatterns = [
    path('', home_page, name='home'),
    path('weather_shipment/', WeatherShipmentView.as_view(), name='weather_shipment'),
    path("admin/", admin.site.urls),
]

urlpatterns += swagger_urls
