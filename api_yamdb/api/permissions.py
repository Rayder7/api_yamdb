from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOnly(BasePermission):
    """Доступ только для админа."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class ReadOnly(BasePermission):
    """Пермишен только для чтения."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAuthorOrModeratorOrReadOnly(BasePermission):
    """
    Пермишен для изменения объекта только модератору, админу или автору.
    В остальном можно только для чтения.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )
