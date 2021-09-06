from django.contrib import admin
from user.models import Watchlist, Wallet, Inventory
from item.models import Currency, Price, Item
from trading.models import Offer, Trade


@admin.register(Watchlist)
class Watchlist(admin.ModelAdmin):
    fields = ('user', 'item')


@admin.register(Wallet)
class Wallet(admin.ModelAdmin):
    fields = ('user', 'currency', 'balance')


@admin.register(Inventory)
class Inventory(admin.ModelAdmin):
    fields = ('user', 'item', 'quantity')


@admin.register(Item)
class Item(admin.ModelAdmin):
    fields = ('code', 'name', 'price', 'currency', 'details')


@admin.register(Currency)
class Currency(admin.ModelAdmin):
    fields = ('name', 'code')


@admin.register(Price)
class Price(admin.ModelAdmin):
    fields = ('currency', 'price', 'item', 'date')


@admin.register(Offer)
class Offer(admin.ModelAdmin):
    fields = ('user', 'item', 'entry_quantity', 'quantity', 'order_type', 'price', 'is_active')


@admin.register(Trade)
class Trade(admin.ModelAdmin):
    fields = ('item', 'seller_offer', 'buyer_offer', 'quantity', 'unit_price', 'description')
# Register your models here.
