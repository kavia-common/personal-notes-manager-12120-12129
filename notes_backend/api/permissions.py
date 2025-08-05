from rest_framework import permissions

# PUBLIC_INTERFACE
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a note to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always allow GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the note
        return obj.user == request.user
