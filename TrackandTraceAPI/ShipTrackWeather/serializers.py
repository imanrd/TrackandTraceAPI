from rest_framework import serializers


class TrackingCarrierSerializer(serializers.Serializer):
    tracking_number = serializers.CharField()
    carrier = serializers.CharField()
