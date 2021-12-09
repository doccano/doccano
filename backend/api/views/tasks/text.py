from ...models import TextLabel
from ...serializers import TextLabelSerializer
from .base import BaseDetailAPI, BaseListAPI


class TextLabelListAPI(BaseListAPI):
    annotation_class = TextLabel
    serializer_class = TextLabelSerializer


class TextLabelDetailAPI(BaseDetailAPI):
    queryset = TextLabel.objects.all()
    serializer_class = TextLabelSerializer
