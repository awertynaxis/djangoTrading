from django.urls import path, re_path
from item.views import ItemListView, ItemDetailView, ItemCreateView, CurrencyListView, CurrencyCreateView, PriceListView

urlpatterns = [
    path('items/', ItemListView.as_view(), name='items-list'),
    re_path(r'^item_detail/(?P<item_id>\d+)$', ItemDetailView.as_view(), name='item-detail'),
    path('item_create/', ItemCreateView.as_view(), name='item-create'),
    path('currencies/', CurrencyListView.as_view(), name='currencies-list'),
    path('currency_create/', CurrencyCreateView.as_view(), name='currency-create'),
    path('price/', PriceListView.as_view(), name='price-list'),
]
