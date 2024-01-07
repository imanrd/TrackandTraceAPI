from django.shortcuts import render
from django.views import View
from .weather_utils import WeatherService
from .queries import get_shipment_by_tracking_number_and_carrier
from ShipTrackWeather import logger
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    @method_decorator(name='post', decorator=swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tracking_number': openapi.Schema(type=openapi.TYPE_STRING),
                'carrier': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['tracking_number', 'carrier']
        ),
        responses={
            200: openapi.Response(
                description="Successful retrieval of weather and shipment data",
                examples={
                    'weather_data':
                        """
                        Weather Information for Paris
                        Temperature: 7.14°C
                        Weather: overcast clouds""",
                    'shipments':
                    """
                    Shipment Details
                    Shipment: TN12345678 - DHL - in-transit
                    Shipment: TN12345678 - DHL - in-transit
                    """
                }
            ),
        }
    ))
    def post(self, request):
        logger.info("Post request received")
        tracking_number = request.POST.get('tracking_number')
        carrier = request.POST.get('carrier')

        shipments = get_shipment_by_tracking_number_and_carrier(tracking_number, carrier)
        location = get_receiver_city(shipments)
        weather_data = WeatherService.get_weather_data(location)

        context = {

            'weather_data': weather_data,
            'shipments': shipments,
        }
        return render(request, self.template_name, context)
