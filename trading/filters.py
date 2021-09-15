from django_filters import rest_framework as filters
from trading.models import Offer


class OfferUserFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user__username', lookup_expr='exact')
    is_active = filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    order_type = filters.CharFilter(field_name='order_type', lookup_expr='exact')

    class Meta:
        model = Offer
        fields = ('user', 'is_active', 'order_type')
