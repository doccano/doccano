from ...models import Span
from ...serializers import SpanSerializer
from .base import BaseDetailAPI, BaseListAPI


class SpanListAPI(BaseListAPI):
    annotation_class = Span
    serializer_class = SpanSerializer


class SpanDetailAPI(BaseDetailAPI):
    queryset = Span.objects.all()
    serializer_class = SpanSerializer
