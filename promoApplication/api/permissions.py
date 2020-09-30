from rest_framework import permissions
from promoApplication.models import User


class IsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow admin for create, edit, delete promo.
    """
    def has_permission(self, request, view):
        current_user = User.objects.get(username=request.user)
        return current_user.is_admin

