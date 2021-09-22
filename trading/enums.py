from enum import Enum


class OrderType(Enum):
    SALE = 'Sale'
    PURCHASE = 'Purchase'

    @classmethod
    def get_order_types(cls):
        return [(tag.value,tag) for tag in cls]
