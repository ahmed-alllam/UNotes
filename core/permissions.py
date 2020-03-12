#  Copyright (c) Code Written and Tested by Ahmed Emad in 12/03/2020, 14:49.

from rest_framework import permissions


class UserProfilePermissions(permissions.BasePermission):
    """The Permission class used by UserProfileView."""

    safe_methods = {'POST', 'HEAD', 'OPTIONS'}

    def has_permission(self, request, view):
        """Checks if request is safe, if not it checks if
        the user is authenticated and has a valid profile.
        """
        if request.method in self.safe_methods:
            return True
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            return True
        return False


class NoteBookPermissions(permissions.BasePermission):
    """The Permission class used by NoteBookView."""

    def has_permission(self, request, view):
        """Checks if the user is authenticated and has a valid profile."""
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            return True
        return False


class NotePermissions(permissions.BasePermission):
    """The Permission class used by NoteView."""

    def has_permission(self, request, view):
        """Checks if the user is authenticated and has a valid profile."""
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            return True
        return False


class NoteAttachmentPermissions(permissions.BasePermission):
    """The Permission class used by NoteAttachmentView."""

    def has_permission(self, request, view):
        """Checks if the user is authenticated and has a valid profile."""
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            return True
        return False
