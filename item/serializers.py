from rest_framework import serializers

from item.models import Currency, Item, Price


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')
        read_only_field = ('id',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('details', 'currency', )
        read_only_field = ('id',)


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_field = ('id',)


class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_field = ('id', )
        depth = 1
    currency = CurrencySerializer()


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        read_only_field = ('id', )
        depth = 1
    currency = CurrencySerializer()
    item = ItemSerializer()
