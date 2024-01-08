from django.db import models


class Shipment(models.Model):
    """
    Model representing a shipment.

    Attributes:
    - tracking_number (CharField): Tracking number for the shipment.
    - carrier (CharField): Carrier information for the shipment.
    - sender_address (TextField): Address of the sender.
    - receiver_address (TextField): Address of the receiver.
    - status (CharField): Status of the shipment.
    """
    tracking_number: str = models.CharField(max_length=100)
    carrier: str = models.CharField(max_length=100)
    sender_address: str = models.TextField()
    receiver_address: str = models.TextField()
    status: str = models.CharField(max_length=50)

    def __str__(self) -> str:
        """
        Returns a string representation of the Shipment instance.
        """
        return f"{self.tracking_number} - {self.carrier} - {self.status}"


class Article(models.Model):
    """
    Model representing an article.

    Attributes:
    - shipment (ForeignKey): ForeignKey to Shipment model.
    - article_name (CharField): Name of the article.
    - article_quantity (IntegerField): Quantity of the article.
    - article_price (DecimalField): Price of the article.
    - SKU (CharField): Stock Keeping Unit of the article.
    """
    shipment: Shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    article_name: str = models.CharField(max_length=100)
    article_quantity: str = models.IntegerField()
    article_price: str = models.DecimalField(max_digits=10, decimal_places=2)
    SKU: str = models.CharField(max_length=50)

    def __str__(self) -> str:
        """
        Returns a string representation of the Article instance.
        """
        return f"{self.article_name} - {self.SKU}"
