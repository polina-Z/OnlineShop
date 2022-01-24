from rest_framework import permissions
from.models import Customer


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.user == request.user or request.user.is_superuser


class IsShopOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        customer = Customer.objects.get(user=request.user)
        return customer.store_owner or request.user.is_superuser


class IsProductOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.shop.owner.user == request.user or request.user.is_superuser

