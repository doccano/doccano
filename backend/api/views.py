from celery.result import AsyncResult
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class TaskStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        task = AsyncResult(kwargs["task_id"])
        ready = task.ready()
        error = ready and not task.successful()

        return Response(
            {
                "ready": ready,
                "result": task.result if ready and not error else None,
                "error": {"text": str(task.result)} if error else None,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class DatabaseHealthCheck(APIView):
    """
    API endpoint para verificar se a base de dados está disponível
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            # Tenta fazer uma query simples para testar a conexão
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            return JsonResponse({
                'status': 'healthy',
                'database': 'connected',
                'message': 'Base de dados disponível'
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'status': 'unhealthy',
                'database': 'disconnected',
                'message': 'Base de dados não disponível',
                'error': str(e)
            }, status=503)
