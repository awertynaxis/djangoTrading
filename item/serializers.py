from rest_framework import serializers
from item.validators import positive_price_validator
from item.models import Currency, Item, Price


class CurrencyDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', )
        read_only_field = ('id',)


class CurrencyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('name', 'code')
        read_only_field = ('id',)


class CurrencyRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('name', 'code', 'is_not_deleted')
        read_only_field = ('id',)


class CurrencyCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('code', 'name')
        read_only_field = ('id',)

    def create(self, validated_data):
        return Currency.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.save(update_fields=('code', 'name'))
        return instance

    @staticmethod
    def validate_code(value):

        if not value.isupper():
            raise serializers.ValidationError('Code must be in upper case')
        return value

    @staticmethod
    def validate_name(value):

        if value == 'PHP':
            raise serializers.ValidationError('Sorry u cant use PHP'
                                              ' for currency naming')
        return value


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('details', )
        read_only_field = ('id',)


class ItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', )
        read_only_field = ('id',)


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('price', 'currency', 'details', 'code', 'name')
        read_only_field = ('id',)

    @staticmethod
    def validate_name(value):

        bad_words = ('Index', 'Forex', 'Bitcoin')
        if value in bad_words:
            raise serializers.ValidationError("sorry, dont "
                                              "use bad words")
        if len(value) > 30:
            raise serializers.ValidationError("length of name "
                                              "must be lower 30 ")
        return value

    @staticmethod
    def validate_code(value):

        if not value.isupper():
            raise serializers.ValidationError("sorry, code must "
                                              "be in upper case")
        return value

    @staticmethod
    def validate_price(value):

        if value > 100.00:
            raise serializers.ValidationError("start price of stock"
                                              " can't be upper 100.00")
        return value


class ItemRetrieveSerializer(serializers.ModelSerializer):

    currency = CurrencyRetrieveSerializer()

    class Meta:
        model = Item
        fields = ('price', 'currency', 'details')
        read_only_field = ('id', )


class PriceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ('price', 'currency', 'item')
        read_only_field = ('id', )


class PriceRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ('price', 'currency', 'item', 'date')
        read_only_field = ('id', )


class PriceUpdateSerializer(serializers.ModelSerializer):

    currency = CurrencyRetrieveSerializer()
    item = ItemListSerializer()
    price = serializers.DecimalField(
        validators=(positive_price_validator,), max_digits=20, decimal_places=2
    )

    class Meta:
        model = Price
        fields = ('price', 'currency', 'item', 'date')
        read_only_field = ('id', )
