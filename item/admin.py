from django.contrib import admin
from item.models import Currency, Price, Item


@admin.register(Item)
class Item(admin.ModelAdmin):
    fields = ('code', 'name', 'price', 'currency', 'details')
    search_fields = ('code', )
    autocomplete_fields = ('currency', )


@admin.register(Currency)
class Currency(admin.ModelAdmin):
    fields = ('name', 'code', 'is_not_deleted')
    search_fields = ('code', 'name', 'is_not_deleted')


@admin.register(Price)
class Price(admin.ModelAdmin):
    fields = ('currency', 'price', 'item', 'date')
    search_fields = ('date', 'currency')
    autocomplete_fields = ('currency', 'item')
