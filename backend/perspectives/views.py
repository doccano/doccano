from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Perspective
from .serializers import PerspectiveSerializer
from projects.models import Project
from rest_framework.permissions import AllowAny, IsAuthenticated

class PerspectiveView(viewsets.ModelViewSet):
    serializer_class = PerspectiveSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Perspective.objects.filter(project_id=project_id)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)