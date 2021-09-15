# # from __future__ import annotations
# from django.db import models
# from django.apps import apps
# from typing import TYPE_CHECKING
# # if TYPE_CHECKING:
# # from user.models import Wallet
# # Wallet = apps.get_model('user', 'Wallet')
#
#
# class UserWalletManager(models.Manager):
#
#     def create(self, user, currency, balance=0):
#         wallet = Wallet(user=user, currency=currency, balance=balance)
#         wallet.save()
#         return wallet

