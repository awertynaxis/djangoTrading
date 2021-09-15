from rest_framework import routers
from trading.views import OfferViewSet, UserTradingViewSet

router = routers.SimpleRouter()

router.register(r'offer', OfferViewSet, basename='offer')
router.register(r'trade', UserTradingViewSet, basename='trade')

urlpatterns = router.urls
