from rest_framework import serializers
from user.models import Wallet, Watchlist, Inventory
from item.models import Currency, Item
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


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
        read_only_fields = ('id',)

    def create(self, validated_data):
        user, currency, balance = (
            validated_data['user'],
            validated_data['currency'],
            validated_data['balance']
        )
        return Wallet.objects.create(
            user=user,
            currency=currency,
            balance=balance
        )

    def validate(self, data):

        if not data['currency'].is_not_deleted:
            raise serializers.ValidationError(
                'Sorry u cant create wallet with unavaible currency'
            )
        data['balance'] = 0
        return data


class WalletDonateSerializer(serializers.ModelSerializer):

    balance = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        min_value=0
    )

    class Meta:
        model = Wallet
        fields = ('balance', )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.balance += validated_data.get('balance', 0)
        instance.save(update_fields=('balance',))
        return instance

    @staticmethod
    def validate_balance(value):

        if value < 0:
            raise serializers.ValidationError('Sorry wrong donate')
        return value


class WalletList(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('user', 'currency', 'balance')
        read_only_fields = ('id',)


class WalletRetrieveSerializer(serializers.ModelSerializer):

    currency = CurrencySerializer()
    user = UserSerializer()

    class Meta:
        model = Wallet
        fields = ('user', 'currency', 'balance')
        read_only_fields = ('id',)


class WalletDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('id', )
        read_only_fields = ('id',)


class InventoryListSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    user = UserSerializer()

    class Meta:
        model = Inventory
        fields = ('user', 'item', 'quantity')
        read_only_fields = ('id',)


class WatchlistRetrieveSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    user = UserSerializer()

    class Meta:
        model = Watchlist
        fields = ('user', 'item')
        read_only_fields = ('id',)


class WatchlistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist
        fields = ('user', 'item')
        read_only_fields = ('id',)
#!/usr/bin/bash

class WatchlistCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist
        fields = ('user', 'item')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user, item = (
            validated_data['user'],
            validated_data['item']
        )
        return Watchlist.objects.create(
            user=user,
            item=item
        )

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item')
        instance.item = item_data
        instance.save(update_fields=('item',))
        return instance


class WatchlistDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Watchlist
        fields = ('id', )
        read_only_fields = ('id',)


class UserWithTokenSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
        read_only_fields = ('id',)

    @staticmethod
    def get_token(obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserWalletsListSerializer(serializers.ModelSerializer):

    wallets = serializers.SlugRelatedField(
        read_only=True,
        slug_field='balance',
        many=True
    )

    class Meta:
        model = User
        fields = ('username', 'wallets')
        read_only_fields = ('id',)
