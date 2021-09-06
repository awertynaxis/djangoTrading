from rest_framework import status
from rest_framework.response import Response
from trading.models import Offer
from trading.serializers import OfferSerializer, OfferCreateSerializer
from trading.filters import OfferUserFilter
from rest_framework.generics import ListAPIView, CreateAPIView


class OfferListView(ListAPIView):
    """Uses to get list of offers with specific filters"""
    model = Offer
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filterset_class = OfferUserFilter


class OfferCreateView(CreateAPIView):
    """Uses to create a new offer"""
    model = Offer
    serializer_class = OfferCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
