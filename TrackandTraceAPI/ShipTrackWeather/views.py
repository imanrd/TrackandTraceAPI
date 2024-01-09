from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .weather_utils import WeatherService
from .queries import get_shipment_by_tracking_number_and_carrier
from ShipTrackWeather import logger
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from typing import Union, List
from .serializers import ShipmentSerializer, TrackingCarrierSerializer
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
    logger.exception(f"Shipments: {shipments}")
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


class WeatherShipmentView(APIView):
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

    @method_decorator(name='get', decorator=swagger_auto_schema(
        operation_id='get_weather_and_shipment_data',
        parameters=[
            openapi.Parameter(
                name='tracking_number',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='The tracking number of the shipment',
                required=True
            ),
            openapi.Parameter(
                name='carrier',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='The carrier of the shipment',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful retrieval of weather and shipment data',
                examples={
                    'weather_data':
                        """
                        Weather Information for Paris
                        Temperature: 7.14°C
                        Weather: overcast clouds
                        """,
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
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the weather shipment view.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered HTML template.
        """
        logger.info("GET request received")
        return Response(status=status.HTTP_200_OK)

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

        This method processes POST requests to retrieve weather and shipment data based on the input provided. It
        expects a payload containing 'tracking_number' and 'carrier' fields. If the request is made from the Swagger
        UI, it allows default values ('TN12345680' for tracking number and 'DPD' for the carrier) to be used if no
        input is provided. The method fetches shipment details and location information based on the provided
        tracking number and carrier, then fetches weather data for that location. Finally, it renders an HTML
        template with the retrieved weather and shipment data.
        """
        logger.info("Post request received")
        serializer = TrackingCarrierSerializer(data=request.data)
        if serializer.is_valid():
            tracking_number = request.POST.get('tracking_number')
            carrier = request.POST.get('carrier')
            referer = request.META.get("HTTP_REFERER")
            logger.info(referer)
            if referer and "swagger" in referer:
                if tracking_number is None and carrier is None:
                    tracking_number = "TN12345680"
                    carrier = "DPD"
            shipments = get_shipment_by_tracking_number_and_carrier(tracking_number, carrier)
            location = get_receiver_city(shipments)
            weather_data = WeatherService.get_weather_data(location)

            context = {

                'weather_data': weather_data,
                'shipments': shipments,
            }
            return render(request, self.template_name, context)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
