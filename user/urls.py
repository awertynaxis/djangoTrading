from rest_framework import routers
from user.views import (
    UserWalletViewSet,
    UserWatchlistViewSet,
    UserInventoryViewSet,
    CreateUserTokenViewSet
)

router = routers.SimpleRouter()

router.register(r'wallet', UserWalletViewSet, basename='wallet')
router.register(r'watchlist', UserWatchlistViewSet, basename='watchlist')
router.register(r'inventory', UserInventoryViewSet, basename='inventory')
router.register(r'create-user', CreateUserTokenViewSet, basename='create-user')

urlpatterns = router.urls
