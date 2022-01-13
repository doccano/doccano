from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Role
from .serializers import RoleSerializer


class Roles(generics.ListAPIView):
    serializer_class = RoleSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
