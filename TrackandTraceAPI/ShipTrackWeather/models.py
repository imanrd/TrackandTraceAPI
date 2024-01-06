from django.db import models


# Create your models here.


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100)
    sender_address = models.TextField()
    receiver_address = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.tracking_number} - {self.carrier} - {self.status}"


class Article(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=100)
    article_quantity = models.IntegerField()
    article_price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.article_name} - {self.SKU}"
