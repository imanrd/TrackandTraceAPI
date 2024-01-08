from django.shortcuts import render
from django.views import View
from .weather_utils import WeatherService
from .queries import get_shipment_by_tracking_number_and_carrier
from ShipTrackWeather import logger
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from typing import Union, List
from django.http import HttpRequest, HttpResponse


def get_receiver_city(shipments: Union[List, None]) -> str:
    """
    Extracts the city from the receiver address of the first shipment.

    Args:
    - shipments: QuerySet of shipments.

    Returns:
    - str: City name extracted from the receiver address.

    Raises:
    - Exception: If no shipments are available or receiver address is missing.
    """

    if shipments and shipments.first().receiver_address:
        receiver_address = shipments.first().receiver_address
        city = receiver_address.split(' ')[-2].strip()
        return city
    raise Exception("No shipments")


def home_page(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page.

    Args:
    - request: HTTP request object.

    Returns:
    - HttpResponse: Rendered HTML template for the home page.
    """

    return render(request, 'template.html')


class WeatherShipmentView(View):
    """
    View for retrieving weather and shipment data.

    Attributes:
    - template_name (str): Name of the HTML template.
    """

    template_name = 'weather_shipment.html'

    def render_template(self, request: HttpRequest) -> HttpResponse:
        """
        Renders the HTML template.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered HTML template.
        """
        return render(request, self.template_name)

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the weather shipment view.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered HTML template.
        """
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
    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles POST requests to retrieve weather and shipment data.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered HTML template with weather and shipment data.
        """
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
