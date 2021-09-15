from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import BlackList


class BlackListPermission(BasePermission):
    """Permisshion checks for banned users"""
    def has_permission(self, request, view):
        user = request.user
        blacklist = BlackList.objects.filter(user=user).first()
        if blacklist is None:
            return True
        else:
            if blacklist.banned is True:
                return False
            if blacklist.banned is False:
                return True


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        # if request.method in SAFE_METHODS:
        #     return True
        if obj.user == request.user:
            return True
        else:
            return False


class CreateOfferPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if int(request.data['user']) is user.id:
            return True
        else:
            return False


class CantDelete(BasePermission):

    def has_object_permission(self, request, view, obj):

        # if request.method in SAFE_METHODS:
        #     return True
        if obj.balance > 0:
            return False
        else:
            return True
