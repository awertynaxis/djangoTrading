from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from item.models import Item, Currency


class Watchlist(models.Model):
    """Current user, favorite list of stocks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username} watchlist'


class Inventory(models.Model):
    """The number of  stocks a particular user has"""
    user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField("Stocks quantity", default=0)

    def __str__(self):
        return f'{self.user.username} has {self.quantity} {self.item}'


class Wallet(models.Model):
    """User's wallet"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet")
    currency = models.ForeignKey(Currency, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    balance = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'{self.user.username} has {self.balance}'
