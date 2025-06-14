from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connections
from django.db.utils import OperationalError

from .serializers import UserSerializer, CustomRegisterSerializer
from projects.permissions import IsProjectAdmin


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class HealthCheck(APIView):
    """
    Endpoint para verificar a saúde da base de dados
    """
    permission_classes = []  # Sem autenticação necessária

    def get(self, request, *args, **kwargs):
        try:
            # Tenta fazer uma query simples para verificar a conexão
            db_conn = connections['default']
            cursor = db_conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            return Response({
                'status': 'healthy',
                'database': 'connected'
            }, status=status.HTTP_200_OK)
            
        except OperationalError:
            return Response({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': 'Database connection failed'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'database': 'error',
                'error': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CheckUserExists(APIView):
    """
    Endpoint para verificar se username ou email já existem
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        user_id = request.data.get('user_id')  # Para excluir na verificação de edição
        
        response_data = {}
        
        if username:
            exists = User.objects.filter(username=username)
            if user_id:
                exists = exists.exclude(id=user_id)
            response_data['username_exists'] = exists.exists()
            
        if email:
            exists = User.objects.filter(email=email)
            if user_id:
                exists = exists.exclude(id=user_id)
            response_data['email_exists'] = exists.exists()
            
        return Response(response_data, status=status.HTTP_200_OK)


class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)


class UserCreation(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        
        # Aplica as permissões de superuser e staff
        cleaned_data = serializer.get_cleaned_data()
        user.is_superuser = cleaned_data.get('is_superuser', False)
        user.is_staff = cleaned_data.get('is_staff', False)
        user.first_name = cleaned_data.get('first_name', '')
        user.last_name = cleaned_data.get('last_name', '')
        
        user.save()
        return user


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserDeletion(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def delete(self, request, *args, **kwargs):
        # Obtém os usuários a partir dos IDs passados na requisição

        # Se apenas um usuário for excluído, obtém o usuário
        user = self.get_object()

        if request.user == user:
            return Response({"detail": "You cannot delete your own account."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()  # Exclui o usuário
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
