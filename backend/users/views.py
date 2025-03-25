from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from .serializers import UserSerializer
from projects.permissions import IsProjectAdmin


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


from rest_framework import filters  # já deve estar aí

class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("username",)

    ordering_fields = ['username','first_name','last_name', 'is_staff', 'is_superuser', 'is_active']  # ADICIONADO
    ordering = ['username']  # ORDEM PADRÃO


    # (Opcional) Se quiser paginação customizada, define aqui
    pagination_class = None


class UserCreation(generics.CreateAPIView):
    serializer_class = RegisterSerializer 
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        if request.data.get('is_superuser') in [True, 'true', 'True', 1]:
            user.is_superuser = True
            user.is_staff = True
            user.save()
        headers = self.get_success_headers(serializer.data)
        if request.data.get('is_staff') in [True, 'true', 'True', 1]:
            user.is_superuser = False
            user.is_staff = True
            user.save()
        if request.data.get('is_staff' and "is_superuser") in [True, 'true', 'True', 1]:
            user.is_superuser = True
            user.is_staff = True
            user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user



class BulkDeleteUsers(generics.GenericAPIView):
    permission_classes = [IsAuthenticated & IsAdminUser]
    parser_classes = [JSONParser]

    # Alteramos para POST
    def post(self, request, *args, **kwargs):
        ids = request.data.get('ids', [])
        if not isinstance(ids, list) or not ids:
            return Response({"detail": "IDs not provided or invalid."}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)