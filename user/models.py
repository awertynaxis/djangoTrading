from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from item.models import Item, Currency
# from user.managers import UserWalletManager


class UserWalletManager(models.Manager):
    """This manager uses to create wallet model in serializer"""
    @staticmethod
    def create(user, currency, balance=0):
        wallet = Wallet(user=user, currency=currency, balance=balance)
        wallet.save()
        return wallet


class UserWatchlistManager(models.Manager):
    """This manager uses to create watchlist model in serializer"""
    @staticmethod
    def create(user, item):
        watchlist = Watchlist(user=user, item=item)
        watchlist.save()
        return watchlist


class Watchlist(models.Model):
    """Current user, favorite list of stocks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, related_name='watch_list')

    objects = UserWatchlistManager()

    def __str__(self):
        return f'{self.user.username} watchlist'


class Inventory(models.Model):
    """The number of  stocks a particular user has"""
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.IntegerField("Stocks quantity", default=0)

    def __str__(self):
        return f'{self.user.username} has {self.quantity} {self.item}'


class Wallet(models.Model):
    """User's wallet"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet')
    currency = models.OneToOneField(Currency, blank=True, null=True, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    objects = UserWalletManager()

    def __str__(self):
        return f'{self.user.username} has {self.balance}'


class BlackList(models.Model):
    """User's blacklist store information about banned users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="black_list")
    banned = models.BooleanField(default=True)

    def __str__(self):
        if self.banned:
            return f'{self.user.username} is banned'
        else:
            return f'{self.user.username} is not banned'
