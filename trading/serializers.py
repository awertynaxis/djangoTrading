from rest_framework import serializers

from trading.models import Offer, Trade
from user.serializers import UserSerializer
from item.serializers import ItemRetrieveSerializer


class OfferRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('is_active',)
        read_only_field = ('id',)
    user = UserSerializer()
    item = ItemRetrieveSerializer()


class OfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('is_active', 'price', 'entry_quantity', 'quantity')
        read_only_field = ('id',)
    user = UserSerializer()
    item = ItemRetrieveSerializer()


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('is_active', )
        read_only_field = ('id',)

    def validate(self, data):
        if data['order_type'] == 'Sale':
            if data['price'] > 1000:
                raise serializers.ValidationError(
                    "u cant target price upper then 1000"
                )
            if data['entry_quantity'] > data['quantity']:
                raise serializers.ValidationError(
                    "u cant sale stocks more than u have"
                )
        if data['order_type'] == 'Purchase' and data['price'] < 10:
            raise serializers.ValidationError("u cant target price lower 10")
        if data['price'] < 0:
            raise serializers.ValidationError(
                "u can enter only positive value"
            )
        if data['item'].currency.is_not_deleted is False:
            raise serializers.ValidationError(
                "u cant use stock with not available currency"
            )
        return data


class TradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('item',
                  'seller_offer',
                  'buyer_offer',
                  'quantity',
                  'unit_price',
                  'description')
        read_only_field = ('id',)


class TradeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('item',
                  'seller_offer',
                  'buyer_offer',
                  'quantity',
                  'unit_price',
                  'description')
        read_only_field = ('id',)
    item = ItemRetrieveSerializer()
    seller_offer = OfferRetrieveSerializer()
    buyer_offer = OfferRetrieveSerializer()
