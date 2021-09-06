from rest_framework import status
from rest_framework.response import Response
from item.models import Item, Currency, Price
from item.serializers import ItemDetailSerializer, ItemSerializer, ItemCreateSerializer, CurrencySerializer, \
    PriceSerializer
from item.filters import ItemNameFilter, PriceItemFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView


class ItemListView(ListAPIView):
    """Uses to view all items in service or item's by name company"""
    model = Item
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filterset_class = ItemNameFilter


class ItemDetailView(RetrieveUpdateDestroyAPIView):
    """Uses to view item detail info and delete it"""
    model = Item
    lookup_field = 'item_id'
    serializer_class = ItemDetailSerializer

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        return Item.objects.get(pk=lookup_field_value)


class ItemCreateView(CreateAPIView):
    """Uses to create a new item"""
    model = Item
    serializer_class = ItemCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CurrencyListView(ListAPIView):
    """Uses to view all available currencies """
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyCreateView(CreateAPIView):
    """Uses to create a new currency """
    model = Currency
    serializer_class = CurrencySerializer


class PriceListView(ListAPIView):
    """Uses to check how price of stock was changed """
    model = Price
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filterset_class = PriceItemFilter
