from rest_framework import mixins, viewsets, status
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from item.models import Item, Currency, Price
from item.serializers import ItemDetailSerializer, ItemSerializer, \
    ItemCreateUpdateSerializer, CurrencySerializer, \
    PriceDetailSerializer, PriceSerializer
from item.filters import ItemNameFilter, PriceItemFilter
from user.permissions import BlackListPermission


class ItemViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """A viewset for model Item that provides `retrieve`,
    `create`, `list`, 'update' and 'delete' actions."""
    model = Item
    queryset = Item.objects.all()
    filterset_class = ItemNameFilter
    serializer_action_classes = {
        'list': ItemSerializer,
        'retrieve': ItemDetailSerializer,
        'create': ItemCreateUpdateSerializer,
        'update': ItemCreateUpdateSerializer,
        'delete': ItemSerializer,
        'partial_update': ItemCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


class CurrencyViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """A viewset for model Currency that provides `retrieve`,
    `create`, update' and `list` actions."""
    model = Currency
    queryset = Currency.objects.is_not_deleted()
    serializer_class = CurrencySerializer

    @action(detail=False, methods=('get', ),
            url_path='all-currency',
            permission_classes=(BlackListPermission,))
    def get_all_currency(self, request) -> Response:
        """Allows to get all  'currency' in system,
         available only for not banned users"""
        queryset = Currency.objects.all()
        serializer = CurrencySerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PriceViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet,
                   ):
    """A viewset for model Price that provides `retrieve`,
    `list`, 'update' and special 'get_filtered_date' actions."""
    model = Price
    queryset = Price.objects.all()
    filterset_class = PriceItemFilter
    serializer_action_classes = {
        'list': PriceSerializer,
        'retrieve': PriceDetailSerializer,
        'update': PriceDetailSerializer,
        'partial_update': PriceDetailSerializer,
        'get_filtered_date': PriceSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    @action(detail=False, methods=('get', ), url_path='filter_q')
    def get_filtered_date(self, request) -> Response:
        """Allows to filter Price by 'item' or 'currency'"""
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            queryset = Price.objects.filter(Q(item=serializer.data['item'])
                                            | Q(currency=serializer.data['currency']))
            serializer_set = self.get_serializer(queryset, many=True)
            return Response(data=serializer_set.data, status=status.HTTP_200_OK)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
