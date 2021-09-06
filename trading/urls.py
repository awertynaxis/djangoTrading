from django.urls import path
from trading.views import OfferListView, OfferCreateView

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offers-list'),
    path('create_offer/', OfferCreateView.as_view(), name='offer-create'),
]
