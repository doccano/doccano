from celery.result import AsyncResult
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TaskStatus(APIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        task = AsyncResult(kwargs['task_id'])
        ready = task.ready()
        error = ready and not task.successful()

        return Response({
            'ready': ready,
            'result': task.result if ready and not error else None,
            'error': {'text': str(task.result)} if error else None,
        })


class TaskTest(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        from .. import tasks
        upload_id = request.GET.get('upload_id')
        task = tasks.parse.delay(upload_id)
        return Response({'task_id': task.task_id})
