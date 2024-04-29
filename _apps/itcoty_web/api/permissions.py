from rest_framework import permissions


class IsUserProfileOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow users edit their profiles.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
