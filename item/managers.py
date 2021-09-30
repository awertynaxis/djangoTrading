from django.db import models
from django.db.models import QuerySet


class CurrencyManager(models.Manager):
    def filter_not_deleted(self) -> QuerySet:
        return self.filter(is_not_deleted=True)
