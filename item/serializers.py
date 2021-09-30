from rest_framework import serializers
from item.validators import positive_price_validator
from item.models import Currency, Item, Price


class CurrencySerializer(serializers.ModelSerializer):
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

        if value != value.upper():
            raise serializers.ValidationError('Code must be in upper case')
        return value

    @staticmethod
    def validate_name(value):

        if value == 'PHP':
            raise serializers.ValidationError('Sorry u cant use PHP'
                                              ' for currency naming')
        return value


class ItemListDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('details', )
        read_only_field = ('id',)


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('price', 'currency', 'details')
        read_only_field = ('id',)

    def validate(self, data):

        bad_words = ('Index', 'Forex', 'Bitcoin')
        if data['price'] > 100.00:
            raise serializers.ValidationError("start price of stock"
                                              " can't be upper 100.00")
        if data['name'] in bad_words:
            raise serializers.ValidationError("sorry, dont "
                                              "use bad words")
        if data['code'] not in data['code'].upper():
            raise serializers.ValidationError("sorry, code must "
                                              "be in upper case")
        if len(data['name']) > 30:
            raise serializers.ValidationError("length of name "
                                              "must be lower 30 ")
        return data


class ItemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('price', 'currency', 'details')
        read_only_field = ('id', )
    currency = CurrencySerializer()


class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price', 'currency', 'details')
        read_only_field = ('id', )


class PriceRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price', 'currency', 'item', 'date')
        read_only_field = ('id', )
    currency = CurrencySerializer()
    item = ItemListDeleteSerializer()
    price = serializers.DecimalField(
        validators=(positive_price_validator,), max_digits=20, decimal_places=2
    )
