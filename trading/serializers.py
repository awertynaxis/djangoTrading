from rest_framework import serializers

from trading.models import Offer, Trade
from user.serializers import UserSerializer
from item.serializers import ItemRetrieveSerializer
from trading.enums import OrderType


class OfferRetrieveSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    item = ItemRetrieveSerializer()

    class Meta:
        model = Offer
        exclude = ('is_active',)
        read_only_fields = ('id',)


class OfferListSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    item = ItemRetrieveSerializer()

    class Meta:
        model = Offer
        exclude = ('is_active', 'price', 'entry_quantity', 'quantity')
        read_only_fields = ('id',)


class OfferCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('is_active', )
        read_only_fields = ('id',)

    def validate(self, data):

        if data['order_type'] == OrderType.SALE.value:
            if data['price'] > 1000:
                raise serializers.ValidationError(
                    "u cant target price upper then 1000"
                )
            if data['entry_quantity'] > data['quantity']:
                raise serializers.ValidationError(
                    "u cant sale stocks more than u have"
                )
        if data['order_type'] == OrderType.PURCHASE.value and data['price'] < 10:
            raise serializers.ValidationError("u cant target price lower 10")
        return data

    @staticmethod
    def validate_price(value):

        if value < 0:
            raise serializers.ValidationError(
                "u can enter only positive value"
            )
        return value

    @staticmethod
    def validate_item(value):

        if not value.currency.is_not_deleted:
            raise serializers.ValidationError(
                "u cant use stock with not available currency"
            )
        return value


class TradeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ('item',
                  'seller_offer',
                  'buyer_offer',
                  'quantity',
                  'unit_price',
                  'description')
        read_only_fields = ('id',)


class TradeRetrieveSerializer(serializers.ModelSerializer):

    item = ItemRetrieveSerializer()
    seller_offer = OfferRetrieveSerializer()
    buyer_offer = OfferRetrieveSerializer()

    class Meta:
        model = Trade
        fields = ('item',
                  'seller_offer',
                  'buyer_offer',
                  'quantity',
                  'unit_price',
                  'description')
        read_only_fields = ('id',)
