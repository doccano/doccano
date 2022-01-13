from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.permissions import IsAnnotationApprover, IsProjectAdmin

from ..models import Example
from ..serializers import ApproverSerializer


class ApprovalAPI(APIView):
    permission_classes = [IsAuthenticated & (IsAnnotationApprover | IsProjectAdmin)]

    def post(self, request, *args, **kwargs):
        approved = self.request.data.get('approved', True)
        example = get_object_or_404(Example, pk=self.kwargs['example_id'])
        example.annotations_approved_by = self.request.user if approved else None
        example.save()
        return Response(ApproverSerializer(example).data)
