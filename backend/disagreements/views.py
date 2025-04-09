from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Disagreement
from .serializers import DisagreementSerializer

class DisagreementViewSet(viewsets.ModelViewSet):
    serializer_class = DisagreementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dataset_item_id = self.request.query_params.get('dataset_item_id')
        if (dataset_item_id):
            return Disagreement.objects.filter(dataset_item_id=dataset_item_id)
        return Disagreement.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        disagreement = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)