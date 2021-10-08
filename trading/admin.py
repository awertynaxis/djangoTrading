from django.contrib import admin
from trading.models import Offer, Trade


@admin.register(Offer)
class Offer(admin.ModelAdmin):
    fields = ('user',
              'item',
              'entry_quantity',
              'quantity',
              'order_type',
              'price',
              'is_active')
    search_fields = ('user', 'order_type', 'is_active')
    autocomplete_fields = ('user', 'item')


@admin.register(Trade)
class Trade(admin.ModelAdmin):
    fields = ('item',
              'seller_offer',
              'buyer_offer',
              'quantity',
              'unit_price',
              'description')
    search_fields = ('seller_offer', 'buyer_offer', 'item')
    autocomplete_fields = ('item', 'seller_offer', 'buyer_offer')
