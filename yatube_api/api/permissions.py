from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAuthenticatedForSafeMethods(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                raise NotAuthenticated()
        return True
