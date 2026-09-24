from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user
