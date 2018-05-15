from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Annotation, Label


class AnnotationView(View):
    template_name = 'annotation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AnnotationAPIView(View):

    def get(self, request, *args, **kwargs):
        annotation_list = Annotation.objects.all()
        paginator = Paginator(annotation_list, 5)

        page = request.GET.get('page')
        annotations = paginator.get_page(page)
        annotations = [a.as_dict() for a in annotations]

        return JsonResponse({'annotations': annotations})

    def post(self, request, *args, **kwargs):
        pass


class LabelAPIView(View):

    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        labels = [l.as_dict() for l in labels]

        return JsonResponse({'labels': labels})
