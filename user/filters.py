from user.models import Wallet, Watchlist, Inventory
from django_filters import rest_framework as filters


class WalletUserFilter(filters.FilterSet):
    username = filters.CharFilter(
        field_name='user__username',
        lookup_expr='exact'
    )

    class Meta:
        model = Wallet
        fields = ('username', )


class WatchlistUserFilter(filters.FilterSet):
    username = filters.CharFilter(
        field_name='user__username',
        lookup_expr='exact'
    )

    class Meta:
        model = Watchlist
        fields = ('username', )


class InventoryUserFilter(filters.FilterSet):
    username = filters.CharFilter(
        field_name='user__username',
        lookup_expr='exact'
    )

    class Meta:
        model = Inventory
        fields = ('username', )
