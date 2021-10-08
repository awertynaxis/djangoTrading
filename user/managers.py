from django.db import models


class UserWalletManager(models.Manager):
    """This manager uses to create wallet model in serializer"""

    @staticmethod
    def create(user, currency, balance=0):
        from user.models import Wallet

        wallet = Wallet(user=user, currency=currency, balance=balance)
        wallet.save()
        return wallet


class UserWatchlistManager(models.Manager):
    """This manager uses to create watchlist model in serializer"""

    @staticmethod
    def create(user, item):
        from user.models import Watchlist
        watchlist = Watchlist(user=user, item=item)
        watchlist.save()
        return watchlist
