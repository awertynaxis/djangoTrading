from rest_framework import serializers


def positive_price_validator(value):
    if value < 0:
        raise serializers.ValidationError('price of stock must be upper 0')
