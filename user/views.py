from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView,  CreateAPIView, \
    RetrieveDestroyAPIView, UpdateAPIView
from django.contrib.auth.models import User
from user.models import Wallet, Watchlist, Inventory
from user.serializers import WalletSerializer, WatchlistSerializer, InventorySerializer, AddItemSerializer, \
    WalletCreateSerializer, WalletDonateSerializer, WatchlistDetailSerializer
from user.filters import WalletUserFilter, WatchlistUserFilter, InventoryUserFilter
from rest_framework.response import Response


class UserWalletListView(ListAPIView):
    """Uses to view user's wallets"""
    model = Wallet
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_class = WalletUserFilter


class UserWalletDeleteView(RetrieveDestroyAPIView):
    """Uses to delete user's wallets"""
    lookup_field = 'wallet_id'
    model = Wallet
    serializer_class = WalletSerializer

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        return Wallet.objects.get(pk=lookup_field_value)

    def destroy(self, request, *args, **kwargs):
        wallet = self.get_object()
        if wallet.balance == 0:
            self.perform_destroy(wallet)
            return Response(status=status.HTTP_200_OK)
        else:
            error_message = {'Error': 'Sorry, u cant delete a wallet which not empty'}
            return Response(data=error_message, status=status.HTTP_418_IM_A_TEAPOT)


class UserWalletDonateView(UpdateAPIView):
    """Uses to donate a money in user's wallet"""
    lookup_field = 'wallet_id'
    model = Wallet
    serializer_class = WalletDonateSerializer

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        return Wallet.objects.get(pk=lookup_field_value)

    def patch(self, request, *args, **kwargs):
        wallet = self.get_object()
        wallet_donate = request.data['balance']
        wallet.balance += wallet_donate
        wallet.save()
        success_message = {'Success': f'u successfull donate {wallet_donate} {wallet.currency} for your wallet'}
        return Response(success_message, status=status.HTTP_200_OK)


class UserWalletAddView(CreateAPIView):
    """Uses to create a wallet for logged user based on existed currencies"""
    model = Wallet
    serializer_class = WalletCreateSerializer

    def perform_create(self, serializer):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        serializer.save(user=user)


class UserWatchlistListView(ListAPIView):
    """Uses to check favourites list of user's items"""
    model = Watchlist
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    filterset_class = WatchlistUserFilter


class AddItemWatchListView(CreateAPIView):
    """Add a new item to user's watchlist"""
    model = Watchlist
    serializer_class = AddItemSerializer

    def perform_create(self, serializer):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        serializer.save(user=user)


class UserWatchlistDeleteView(RetrieveUpdateDestroyAPIView):
    """Uses to delete to check detail information about item in watchlist and delete"""
    model = Watchlist
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistDetailSerializer
    http_method_names = ['get', 'head', 'delete']


class UserInventoryListView(ListAPIView):
    """Uses to check a user's current items in inventory"""
    model = Inventory
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filterset_class = InventoryUserFilter
