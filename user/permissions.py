from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.is_superuser


class IsApprovedUser(BasePermission):
    def has_permission(self, request, view):
        return request.is_staff