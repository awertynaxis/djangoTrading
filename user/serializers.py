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
        fields = ('currency', 'user')
        read_only_field = ('id',)

    def create(self, validated_data):
        return Wallet.objects.create(
            user=validated_data['user'],
            currency=validated_data['currency'],
            balance=validated_data['balance']
        )

    def validate(self, data):

        if data['currency'].is_not_deleted is False:
            raise serializers.ValidationError('Sorry u cant create wallet with unavaible currency')
        data['balance'] = 0
        return data


class WalletDonateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance', )
    balance = serializers.DecimalField(max_digits=20, decimal_places=2)

    def update(self, instance, validated_data):
        instance.balance += validated_data.get('balance', instance.balance)
        instance.save()
        return instance

    @staticmethod
    def validate_balance(value):

        if value < 0:
            raise serializers.ValidationError('Sorry wrong donate')
        return value


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_field = ('id',)
    currency = CurrencySerializer()
    user = UserSerializer()


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_field = ('id',)
    item = ItemSerializer()
    user = UserSerializer()


class WatchlistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'
        read_only_field = ('id',)
    item = ItemSerializer()
    user = UserSerializer()


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('user', 'item')
        read_only_field = ('id',)

    def create(self, validated_data):
        return Watchlist.objects.create(
            user=validated_data['user'],
            item=validated_data['item']
        )

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item')
        instance.item = item_data
        instance.save()
        return instance
