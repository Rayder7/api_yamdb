from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


#class OwnerOrModeratorOrAdminUserPermission(BasePermission):

#   def has_object_permission(self, request, view, obj):
#        if request.method in ('PATCH', 'DELETE'):
#            return (request.user == obj.author) or (request.user and request.user.is_staff)
#        return (request.method in SAFE_METHODS
#                or request.user == obj.author)
