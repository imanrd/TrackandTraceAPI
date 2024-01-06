from django.shortcuts import render
from .weather_utils import get_weather_data
from .queries import get_shipment_by_tracking_number_and_carrier


def home_page(request):
    return render(request, 'template.html')


def shipment_result(request):
    tracking_number = request.GET.get('tracking_number')
    carrier = request.GET.get('carrier')

    shipments = get_shipment_by_tracking_number_and_carrier(tracking_number, carrier)

    return render(request, 'shipment_result.html', {'shipments': shipments})


def weather_view(request):
    location = "Madrid, Spain"
    weather_data = get_weather_data(location)
    return render(request, "weather.html", {'weather_data': weather_data})
