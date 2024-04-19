from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customers to create orders.
    """

    def has_permission(self, request, view):
        return not request.user.is_staff
