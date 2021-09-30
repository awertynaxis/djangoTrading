import pytest
from django.urls import reverse
from item.models import Item, Currency
from item.serializers import ItemRetrieveSerializer
import factory
from pytest_factoryboy import register
from django_factories import Factory


@register
class SuperFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
    code = 'GO'
    name = 'Gorecka'


def test_currency_factory(currency_super):
    assert isinstance(currency_super, Currency)


@pytest.fixture
def currency_factory(request, db):
    factorie = Factory(Currency)
    return factorie(request)


@pytest.mark.django_db
def test_my_item(currency_factory):
    currency = currency_factory()
    assert currency is not None
    assert Currency.objects.count() == 1


@pytest.mark.django_db
def test_item_serializer(data):
    serializer = ItemRetrieveSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_item_list_view(client, item: Item):
    url = reverse('items-list')
    responce = client.get(url)
    assert responce.status_code == 200
    assert Item.objects.count() == 1
    assert Item.objects.filter(name=item.name)


@pytest.mark.django_db
def test_item_create_view(client, data):
    url = reverse('item-create')
    responce = client.post(url, data=data)
    assert responce.status_code == 201
    assert Item.objects.count() == 1
    assert Item.objects.filter(name=data['name'])


@pytest.mark.django_db
def test_item_detail_view(client, item: Item):
    url = reverse('item-detail', kwargs={'item_id': item.id})
    response = client.get(url)
    assert response.status_code == 200
    assert Item.objects.count() == 1
    assert Item.objects.filter(name=item.name)
    assert item.name in response.content.decode()


@pytest.mark.django_db
def test_currency_list_view(client, currency: Currency):
    url = reverse('currencies-list')
    responce = client.get(url)
    assert responce.status_code == 200
    assert Currency.objects.count() == 1
    assert Currency.objects.filter(code=currency.code)
