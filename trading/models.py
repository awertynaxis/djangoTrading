from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from item.models import Item
from trading.enums import OrderType


class Offer(models.Model):
    """Request to buy or sell specific stocks"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    entry_quantity = models.IntegerField(
        "Requested quantity",
        validators=[MinValueValidator(1)]
    )
    quantity = models.IntegerField("Current quantity", default=0)
    order_type = models.CharField(
        max_length=20,
        choices=OrderType.get_order_types()
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.order_type} {self.item.code} by {self.user.username}'


class Trade(models.Model):
    """Information about a certain transaction"""
    item = models.ForeignKey(
        Item,
        null=True,
        on_delete=models.CASCADE,
        related_name='trade'
    )
    seller_offer = models.ForeignKey(Offer,
                                     null=True,
                                     related_name='seller_trade',
                                     on_delete=models.CASCADE)
    buyer_offer = models.ForeignKey(Offer,
                                    null=True,
                                    related_name='buyer_trade',
                                    on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f'Trade {self.id}'
