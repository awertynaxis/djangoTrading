from django.contrib import admin
from user.models import Wallet, Watchlist, Inventory, BlackList


@admin.register(Watchlist)
class Watchlist(admin.ModelAdmin):
    fields = ('user', 'item')
    search_fields = ('user', )


@admin.register(Wallet)
class Wallet(admin.ModelAdmin):
    fields = ('user', 'currency', 'balance')
    search_fields = ('user', 'currency')
    autocomplete_fields = ('user', 'currency')


@admin.register(Inventory)
class Inventory(admin.ModelAdmin):
    fields = ('user', 'item', 'quantity')
    search_fields = ('user', 'item')
    autocomplete_fields = ('user', 'item')


@admin.register(BlackList)
class BlackList(admin.ModelAdmin):
    fields = ('user', 'banned')
    search_fields = ('user', )
