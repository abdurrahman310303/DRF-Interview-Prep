from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Permission to only allow admin users."""
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class IsModeratorUser(permissions.BasePermission):
    """Permission to only allow moderator or admin users."""
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_moderator)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to only allow owners of an object to edit it."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or admin
        return obj == request.user or request.user.is_admin

class IsOwnerOrModerator(permissions.BasePermission):
    """Permission to only allow owners or moderators to edit an object."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are allowed to the owner, moderator, or admin
        return obj == request.user or request.user.is_moderator

class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission to only allow admins to edit, but anyone to read."""
    
    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission to only allow owners or admins to access an object."""
    
    def has_object_permission(self, request, view, obj):
        # Admin users can access everything
        if request.user.is_admin:
            return True
        
        # Regular users can only access their own objects
        return obj == request.user
