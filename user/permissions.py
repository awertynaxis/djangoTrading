from rest_framework.permissions import BasePermission
from user.models import BlackList


class BlackListPermission(BasePermission):
    """Permisshion checks for banned users"""
    def has_permission(self, request, view):
        user = request.user
        blacklist = BlackList.objects.filter(user=user).first()
        return not blacklist


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class CreateOfferPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return int(request.data['user']) == user.id


class CantDelete(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.balance <= 0
