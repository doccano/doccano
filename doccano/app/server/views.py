import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Annotation, Label, RawData


class AnnotationView(View):
    template_name = 'annotation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AnnotationAPIView(View):

    def get(self, request, *args, **kwargs):
        once_active_learned = len(Annotation.objects.all().exclude(prob=None)) > 0
        if once_active_learned:
            # Use Annotation model & RawData model.
            # Left outer join data and annotation.
            # Filter manual=False
            # Sort prob
            docs = Annotation.objects.all()
        else:
            # Left outer join data and annotation.
            docs = RawData.objects.filter(annotation__isnull=True)
            docs = [{**d.as_dict(), **{'labels': []}} for d in docs]

        return JsonResponse({'data': docs})

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        data_id, label_id = body.get('id'), body.get('label_id')  # {id:0, label_id:1}

        data = RawData.objects.get(id=data_id)
        label = Label.objects.get(id=label_id)
        Annotation(data=data, label=label, manual=True).save()

        return JsonResponse({})

    def delete(self, request, *args, **kwargs):
        body = json.loads(request.body)
        data_id, label_id = body.get('id'), body.get('label_id')  # {id:0, label_id:1}
        Annotation.objects.get(data=data_id, label=label_id).delete()

        return JsonResponse({})


class MetaInfoAPI(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        labels = [l.as_dict() for l in labels]
        total = RawData.objects.count()
        remaining = RawData.objects.filter(annotation__isnull=True).count()

        return JsonResponse({'labels': labels, 'total': total, 'remaining': remaining})
