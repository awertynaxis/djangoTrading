from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from trading.models import Offer, Trade
from user.permissions import (
    BlackListPermission,
    IsOwner,
    CreateOfferPermission
)
from trading.serializers import (
    OfferRetrieveSerializer,
    OfferCreateSerializer,
    OfferListSerializer,
    TradeListSerializer,
    TradeRetrieveSerializer
)
from trading.filters import OfferUserFilter


class OfferViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """A viewset for model Offer that provides `retrieve`,
     `create`, and `list` actions with specific permissions by action."""
    model = Offer
    queryset = Offer.objects.all()
    filterset_class = OfferUserFilter
    permission_classes = (IsAuthenticated, BlackListPermission)

    serializer_action_classes = {
        'list': OfferListSerializer,
        'retrieve': OfferRetrieveSerializer,
        'create': OfferCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    permission_classes_by_action = {'create': (
                                        IsAuthenticated,
                                        CreateOfferPermission,
                                    ),
                                    'list': (IsAuthenticated,),
                                    'retrieve': (
                                        IsAuthenticated,
                                        BlackListPermission,
                                        IsOwner
                                    ),
                                    }

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class UserTradingViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """A viewset for model Offer that provides `retrieve`,
      `list` and special  actions: 'get_sellers_trade' and 'get_buyers_trade'
      with specific permissions."""
    model = Trade
    queryset = Trade.objects.all()
    permission_classes = (IsAuthenticated, BlackListPermission)

    serializer_action_classes = {
        'list': TradeListSerializer,
        'retrieve': TradeRetrieveSerializer,
        'get_sellers_trade': TradeRetrieveSerializer,
        'get_buyers_trade': TradeRetrieveSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    @action(detail=False, methods=('get',), url_path='sellers')
    def get_sellers_trade(self, request) -> Response:
        """Allows to get all trades by user
         where he was like seller of stocks"""
        sale_trade = Trade.objects.filter(
            seller_offer__user__username=request.user
        )
        serializer = self.get_serializer(sale_trade, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('get',), url_path='buyers')
    def get_buyers_trade(self, request) -> Response:
        """Allows to get all trades by user
         where he was like buyer of stocks"""
        sale_trade = Trade.objects.filter(
            buyer_offer__user__username=request.user
        )
        serializer = self.get_serializer(sale_trade, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
