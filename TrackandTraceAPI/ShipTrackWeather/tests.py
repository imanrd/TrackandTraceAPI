from .models import Shipment, Article
from .queries import get_shipment_by_tracking_number_and_carrier
from django.test import TestCase, RequestFactory
from .views import WeatherShipmentView
from rest_framework.test import APITestCase
from ShipTrackWeather import logger


class WeatherShipmentViewTestCase(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_request(self):
        view = WeatherShipmentView.as_view()
        request = self.factory.get('/weather')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_request(self):
        url = '/weather_shipment'
        data = {
            'tracking_number': 'TN12345678',
            'carrier': 'DHL'
        }
        response = self.client.post(url, data, follow=True)

        logger.info(f"test response: {str(response)}")

        self.assertEqual(response.status_code, 200)


class ShipmentRetrievalTestCase(TestCase):
    def setUp(self):
        shipment = Shipment.objects.create(
            tracking_number='TN12345678',
            carrier='DHL',
            sender_address='Street 1, 10115 Berlin, Germany',
            receiver_address='Street 10, 75001 Paris, France',
            status='in-transit'
        )

        Article.objects.create(
            shipment=shipment,
            article_name='Laptop',
            article_quantity='1',
            article_price='800',
            SKU='LP123'
        )
        Article.objects.create(
            shipment=shipment,
            article_name='Mouse',
            article_quantity='1',
            article_price='25',
            SKU='MO456'
        )

    def test_get_shipment_by_tracking_number_and_carrier(self):
        tracking_number = 'TN12345678'
        carrier = 'DHL'

        result = get_shipment_by_tracking_number_and_carrier(tracking_number, carrier)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Shipment)

    def test_get_shipment_nonexistent(self):
        tracking_number = 'NonExistentNumber'
        carrier = 'NonExistentCarrier'

        result = get_shipment_by_tracking_number_and_carrier(tracking_number, carrier)
        self.assertEqual(len(result), 0)
