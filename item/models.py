from django.db import models


class StockBase(models.Model):
    """Base class template"""
    code = models.CharField("Code", max_length=8, unique=True)
    name = models.CharField("Name", max_length=128, unique=True)

    class Meta:
        abstract = True


class Currency(StockBase):
    """Currency"""

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.code


class Item(StockBase):
    """Particular stock"""
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    details = models.TextField("Details", blank=True, null=True, max_length=512)

    def __str__(self):
        return self.code


class Price(models.Model):
    """Item prices"""
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.item.name} {self.price} for time: {self.date}'
