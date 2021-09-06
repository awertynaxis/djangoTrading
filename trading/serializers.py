from rest_framework import serializers

from trading.models import Offer, Trade
from user.serializers import UserSerializer
from item.serializers import ItemSerializer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('is_active',)
        read_only_field = ('id',)
        depth = 1
    user = UserSerializer()
    item = ItemSerializer()


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_field = ('id',)


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_field = ('id',)
        depth = 1
    item = ItemSerializer()
    seller_offer = UserSerializer()
    buyer_offer = UserSerializer()
