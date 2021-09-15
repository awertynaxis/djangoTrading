from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from user.models import Wallet, Watchlist, Inventory
from item.models import Item
from trading.models import Offer
from user.serializers import WalletSerializer, WatchlistSerializer, InventorySerializer, \
    WalletCreateSerializer, WalletDonateSerializer, WatchlistDetailSerializer
from user.filters import WalletUserFilter, WatchlistUserFilter, InventoryUserFilter
from rest_framework.response import Response
from user.permissions import IsOwner, CantDelete


class UserWalletViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """A viewset for model Wallet that provides `retrieve`, `create`,
     `list`, 'update' and 'delete' actions with specific permissions."""
    model = Wallet
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_class = WalletUserFilter
    permission_classes = (CantDelete, IsOwner)

    serializer_action_classes = {
        'list': WalletSerializer,
        'retrieve': WalletSerializer,
        'create': WalletCreateSerializer,
        'update': WalletDonateSerializer,
        'delete': WalletSerializer,
        'partial_update': WalletDonateSerializer
    }

    permission_classes_by_action = {'create': (IsAuthenticated,),
                                    'list': (IsAuthenticated,),
                                    'delete': (CantDelete, IsAuthenticated, IsOwner),
                                    'retrieve': (IsAuthenticated,),
                                    'update': (IsAuthenticated, IsOwner),
                                    'partial_update': (IsAuthenticated,)
                                    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class UserWatchlistViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """A viewset for model Watchlist that provides `retrieve`, `create`,
     `list`, 'update' and 'delete' actions."""
    model = Watchlist
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    filterset_class = WatchlistUserFilter

    serializer_action_classes = {
        'list': WatchlistSerializer,
        'retrieve':  WatchlistDetailSerializer,
        'create': WatchlistSerializer,
        'delete': WatchlistSerializer,
        'update': WatchlistSerializer,
        'partial_update': WatchlistSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]


class UserInventoryViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """Uses to check a user's current items in inventory and
    via action 'get_statistics' can get some stats"""
    model = Inventory
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filterset_class = InventoryUserFilter

    serializer_action_classes = {
        'list': WatchlistSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def list(self, request, *args, **kwargs):
        queryset = Inventory.objects.filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=('get',), url_path='user-statistics', permission_classes=(IsAuthenticated,))
    def get_statistics(self, request) -> Response:
        """Allows to get stats for user"""
        stocks_number = Item.objects.all().count()
        watchlist_number = Watchlist.objects.filter(user=request.user).count()
        wallet_number = Wallet.objects.filter(user=request.user).count()
        sales_number = Offer.objects.filter(user=request.user, order_type='Sale').count()
        purchase_number = Offer.objects.filter(user=request.user, order_type='Purchase').count()
        statistic = {'stocks': stocks_number,
                     'watchlist': watchlist_number,
                     'wallets': wallet_number,
                     'sales': sales_number,
                     'purchases': purchase_number}
        return Response(data=statistic, status=status.HTTP_200_OK)
