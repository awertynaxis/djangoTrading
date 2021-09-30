import pytest
from typing import Dict, Union
from item.models import Item, Currency
from pytest_factoryboy import register
from django_factories import Factory
import factory
faker = Factory.create()


class CurrencyFactory(factory.django.DjangoModelFactory):
    name = 'Euro'
    code = 'EU'

    class Meta:
        model = 'item.Currency'


fixture = register(CurrencyFactory)


@pytest.fixture
def currency_factory(request, db):
    defaults = {
        'code': 'EU',
        'name': 'Euro'
    }
    return Factory(Currency, **defaults)(request)


@pytest.fixture
def data() -> Dict[str, Union[str, int]]:
    data = {
        'id': 1,
        'code': 'Hol',
        'name': 'Gob',
        'price': 20
    }
    return data


@pytest.fixture
def currency(db) -> Currency:
    currency = Currency.objects.create(code='USD', name='Dollars')
    return currency


@pytest.fixture
def item(db, currency: Currency) -> Item:
    item = Item.objects.create(
        code='Sos',
        name='Soska',
        price=20,
        currency=currency)
    return item
