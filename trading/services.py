from trading.enums import OrderType
from trading.models import Offer, Trade
from user.models import Inventory, Wallet
from django.db import transaction


class TradeService:
    def __init__(self):
        self.buyer_offers = Offer.objects.filter(
            is_active=True,
            order_type=OrderType.PURCHASE.value
        )
        self.seller_offers = Offer.objects.filter(
            is_active=True,
            order_type=OrderType.SALE.value,
        )

    @staticmethod
    def _update_offer(buyer_offer: Offer, seller_offer: Offer, quantity: int):

        if quantity >= buyer_offer.entry_quantity:
            buyer_offer.entry_quantity = 0
            buyer_offer.is_active = False
            buyer_offer.save(update_fields=('entry_quantity', 'is_active'))
            seller_offer.entry_quantity -= quantity
            if seller_offer.entry_quantity > 0:
                seller_offer.save(update_fields=('entry_quantity',))
            else:
                seller_offer.is_active = False
                seller_offer.save(update_fields=(
                    'entry_quantity',
                    'is_active'
                ))
        else:
            buyer_offer.entry_quantity -= quantity
            buyer_offer.save(update_fields=('entry_quantity',))
            seller_offer.entry_quantity = 0
            seller_offer.is_active = False
            seller_offer.save(update_fields=('entry_quantity', 'is_active'))

    @staticmethod
    def _update_inventory(buyer_offer: Offer,
                          seller_offer: Offer,
                          quantity: int):

        inventory_buyer = Inventory.objects.filter(
            item=buyer_offer.item,
            user=buyer_offer.user
        ).first()
        inventory_buyer.quantity += quantity
        inventory_buyer.save(update_fields=('quantity',))

        inventory_seller = Inventory.objects.filter(
            item=seller_offer.item,
            user=seller_offer.user
        ).first()
        inventory_seller.quantity -= quantity
        inventory_seller.save(update_fields=('quantity',))

    @staticmethod
    def _update_wallet(buyer_offer: Offer, seller_offer: Offer, quantity: int):

        wallet_buyer = Wallet.objects.filter(
            currency__item=buyer_offer.item,
            user=buyer_offer.user
        ).first()
        wallet_buyer.balance -= seller_offer.price * quantity
        wallet_buyer.save(update_fields=('balance',))

        wallet_seller = Wallet.objects.filter(
            currency__item=seller_offer.item,
            user=seller_offer.user
        ).first()
        wallet_seller.balance += seller_offer.price * quantity
        wallet_seller.save(update_fields=('balance',))

    def _update_all_fields(self,
                           buyer_offer: Offer,
                           seller_offer: Offer,
                           quantity: int):

        self._update_inventory(
            buyer_offer=buyer_offer,
            seller_offer=seller_offer,
            quantity=quantity
        )
        self._update_wallet(
            buyer_offer=buyer_offer,
            seller_offer=seller_offer,
            quantity=quantity
        )
        self._update_offer(
            buyer_offer=buyer_offer,
            seller_offer=seller_offer,
            quantity=quantity
        )

    def make_trade(self):
        trades_list = []
        for buyer_offer in self.buyer_offers:
            while buyer_offer.entry_quantity != 0:
                seller_offer = self.seller_offers.filter(
                    item=buyer_offer.item,
                    price__lte=buyer_offer.price,
                    is_active=True,
                    order_type=OrderType.SALE.value,
                    ).order_by('price').first()
                if seller_offer is None:
                    break
                quantity = min(buyer_offer.entry_quantity,
                               seller_offer.entry_quantity)
                trade = Trade(
                    item=buyer_offer.item,
                    seller_offer=seller_offer,
                    buyer_offer=buyer_offer,
                    quantity=quantity,
                    unit_price=buyer_offer.price
                )
                trades_list.append(trade)
                with transaction.atomic():
                    self._update_all_fields(
                        seller_offer=seller_offer,
                        buyer_offer=buyer_offer,
                        quantity=quantity
                    )
        Trade.objects.bulk_create(trades_list)
