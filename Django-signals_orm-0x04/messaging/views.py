from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import logout

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(self, request):
    user = request.user
    user.delete()
    logout(request)
    return Response({"message": "User deleted successfully"},status=status.HTTP_204_NO_CONTENT)


