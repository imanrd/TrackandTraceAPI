from .models import Shipment


def get_shipment_by_tracking_number_and_carrier(tracking_number, carrier):
    try:
        shipments = Shipment.objects.filter(tracking_number=tracking_number, carrier=carrier)
        for shipment in shipments:
            articles = shipment.article_set.all()
            article_names = [article.article_name for article in articles]
            setattr(shipment, 'article_names', article_names)
        return shipments
    except Shipment.DoesNotExist:
        return None
