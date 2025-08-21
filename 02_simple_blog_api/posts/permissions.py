from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors of a post to edit it."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow comment authors to edit their comments."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the comment author
        return obj.author == request.user
