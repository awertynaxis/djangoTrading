from rest_framework import serializers

from item.models import Currency, Item, Price


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')
        read_only_field = ('id',)

    code = serializers.CharField(max_length=8)
    name = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return Currency.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    @staticmethod
    def validate_code(value):

        if value not in value.upper():
            raise serializers.ValidationError('Code must be in upper case')
        return value

    @staticmethod
    def validate_name(value):

        if value == 'Huy':
            raise serializers.ValidationError('Sorry u cant use Huy'
                                              ' for currency naming')
        return value


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('details', )
        read_only_field = ('id',)


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_field = ('id',)

    def validate(self, data):

        bad_words = ('Fuck', 'Cunt', 'Dick')
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


class ItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_field = ('id', )
    currency = CurrencySerializer()


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        read_only_field = ('id', )


def positive_price(value):
    if value < 0:
        raise serializers.ValidationError('price of stock must be upper 0')


class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        read_only_field = ('id', )
    currency = CurrencySerializer()
    item = ItemSerializer()
    price = serializers.DecimalField(validators=(positive_price,),
                                     max_digits=20,
                                     decimal_places=2)
