from rest_framework import permissions

class IsParticipantOrOwner(permissions.BasePermission):
    """Allows only participants to """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        if hasattr(obj,'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

class IsParticipantOfConversation(permissions.BasePermission):
    """Allows only participants to send update delete"""
    def has_permission(self, request, view):
        """Allow access only if the user is authenticated"""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'conversation'):
            if (request.method in ["PUT", "PATCH", "DELETE", "POST"] or request.method == "GET"):
                return request.user in obj.conversation.participants.all()

        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False