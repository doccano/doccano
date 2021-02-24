from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions import IsProjectAdmin
from ..serializers import UserSerializer


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class Users(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serialized_data = UserSerializer(queryset, many=True).data
        return Response(serialized_data)
