from rest_framework import permissions
from promoApplication.models import User


class IsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow admin for create, edit, delete promo.
    """
    def has_permission(self, request, view):
        current_user = User.objects.get(username=request.user)
        return current_user.is_admin


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow normal user for his own promo data.
    """
    def has_object_permission(self, request, view, obj):
        current_user = User.objects.get(username=request.user)
        return current_user.user == obj.user
