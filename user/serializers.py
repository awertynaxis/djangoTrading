from rest_framework import serializers

from user.models import Wallet, Watchlist, Inventory
from item.models import Currency, Item
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'code',)


class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('currency', )
        read_only_field = ('id',)


class WalletDonateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', )
    balance = serializers.DecimalField(max_digits=20, decimal_places=2)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_field = ('id',)
        depth = 1
    currency = CurrencySerializer()
    user = UserSerializer()


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_field = ('id',)
        depth = 1
    item = ItemSerializer()
    user = UserSerializer()


class WatchlistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'
        read_only_field = ('id',)
        depth = 1
    item = ItemSerializer()
    user = UserSerializer()


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'
        read_only_field = ('id',)


class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('item', )
