from rest_framework import serializers

from trading.models import Offer, Trade
from user.serializers import UserSerializer
from item.serializers import ItemSerializer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('is_active',)
        read_only_field = ('id',)
    user = UserSerializer()
    item = ItemSerializer()


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('is_active', )
        read_only_field = ('id',)

    def validate(self, data):
        if data['order_type'] == 'Sale':
            if data['price'] > 1000:
                raise serializers.ValidationError("u cant target price upper then 1000")
            if data['entry_quantity'] > data['quantity']:
                raise serializers.ValidationError("u cant sale stocks more than u have")
        if data['order_type'] == 'Purchase':
            if data['price'] < 10:
                raise serializers.ValidationError("u cant target price lower 10")
        if data['price'] < 0:
            raise serializers.ValidationError("u can enter only positive value")
        if data['item'].currency.is_not_deleted is False:
            raise serializers.ValidationError("u cant use stock with not available currency")
        return data


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_field = ('id',)


class TradeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_field = ('id',)
    item = ItemSerializer()
    seller_offer = OfferSerializer()
    buyer_offer = OfferSerializer()
