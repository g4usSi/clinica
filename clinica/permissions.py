
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permite acceso únicamente a administradores.

    Se considera administrador si:
    - is_staff = True
    o
    - is_superuser = True
    """

    message = "No tienes permisos de administrador."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
            )
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Permite al usuario acceder a su propio registro
    o al administrador acceder a cualquier registro.
    """

    message = "No tienes permisos para acceder a este recurso."

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj == request.user

