from django.shortcuts import render
from django.views import View
from .weather_utils import get_weather_data
from .queries import get_shipment_by_tracking_number_and_carrier
from ShipTrackWeather import logger


def get_receiver_city(shipments):
    if shipments and shipments.first().receiver_address:
        receiver_address = shipments.first().receiver_address
        city = receiver_address.split(' ')[-2].strip()
        return city
    raise Exception("No shipments")


def home_page(request):
    return render(request, 'template.html')


class WeatherShipmentView(View):
    template_name = 'weather_shipment.html'

    def render_template(self, request):
        return render(request, self.template_name)

    def get(self, request):
        logger.info("GET request received")
        return self.render_template(request)

    def post(self, request):
        logger.info("Post request received")
        tracking_number = request.POST.get('tracking_number')
        carrier = request.POST.get('carrier')

        shipments = get_shipment_by_tracking_number_and_carrier(tracking_number, carrier)
        location = get_receiver_city(shipments)
        weather_data = get_weather_data(location)

        context = {

            'weather_data': weather_data,
            'shipments': shipments,
        }
        return render(request, self.template_name, context)
