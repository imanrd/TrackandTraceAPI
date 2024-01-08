from .models import Shipment
from typing import Optional


def get_shipment_by_tracking_number_and_carrier(tracking_number: str, carrier: str) -> Optional[Shipment]:
    """
    Retrieves shipments based on tracking number and carrier, with associated article names.

    Args:
    - tracking_number (str): The tracking number to search for.
    - carrier (str): The carrier to search for.

    Returns:
    - Shipment or None: QuerySet of shipments if found, else None.
    """
    try:
        shipments = Shipment.objects.filter(tracking_number=tracking_number, carrier=carrier)
        for shipment in shipments:
            articles = shipment.article_set.all()
            article_names = [article.article_name for article in articles]
            setattr(shipment, 'article_names', article_names)
        return shipments
    except Shipment.DoesNotExist:
        return None
