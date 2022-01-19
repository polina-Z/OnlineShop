from rest_framework import permissions


class IsShopOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.store_owner
