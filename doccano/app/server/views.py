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
        label_list = Label.objects.all()
        paginator = Paginator(annotation_list, 5)

        page = request.GET.get('page')
        annotations = paginator.get_page(page)
        JsonResponse({'annotations': annotations.object_list, 'labels': label_list})

    def post(self, request, *args, **kwargs):
        pass
