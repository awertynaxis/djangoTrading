from django_filters import rest_framework as filters
from item.models import Price, Item


class ItemNameFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='exact')
    currency = filters.CharFilter(field_name='currency__code',
                                  lookup_expr='exact')

    class Meta:
        model = Item
        fields = ('name', 'currency')


class PriceItemFilter(filters.FilterSet):
    item = filters.CharFilter(field_name='item__name', lookup_expr='exact')

    class Meta:
        model = Price
        fields = ('item', )
