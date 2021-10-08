from rest_framework import routers
from item.views import ItemViewSet, CurrencyViewSet, PriceViewSet

router = routers.SimpleRouter()

router.register(r'stock', ItemViewSet, basename='stock')
router.register(r'currency', CurrencyViewSet, basename='currency')
router.register(r'price', PriceViewSet, basename='price')

urlpatterns = router.urls
