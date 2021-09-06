from django.urls import path, re_path
from user.views import UserWalletListView, UserWatchlistListView, UserInventoryListView, UserWatchlistDeleteView, \
    AddItemWatchListView, UserWalletAddView, UserWalletDeleteView, UserWalletDonateView

urlpatterns = [
    path('wallet/', UserWalletListView.as_view(), name='wallet-list'),
    path('add_wallet/', UserWalletAddView.as_view(), name='wallet-add'),
    re_path(r'^wallet_delete/(?P<wallet_id>\d+)$', UserWalletDeleteView.as_view(), name='wallet-delete'),
    re_path(r'^wallet_donate/(?P<wallet_id>\d+)$', UserWalletDonateView.as_view(), name='wallet-donate'),
    path('watchlist/', UserWatchlistListView.as_view(), name='watch-list'),
    re_path(r'^watchlist/(?P<pk>\d+)$', UserWatchlistDeleteView.as_view(), name='watchlist-detail'),
    path('add_item/', AddItemWatchListView.as_view(), name='add-item'),
    path('inventory/', UserInventoryListView.as_view(), name='inventory-list'),
]
