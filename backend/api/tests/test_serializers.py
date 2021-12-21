# from django.test import TestCase
#
# from ..models import SEQUENCE_LABELING, Label
# from ..serializers import LabelSerializer
# from .api.utils import prepare_project

# class TestLabelSerializer(TestCase):
#
#     def test_create_label(self):
#         project = prepare_project(SEQUENCE_LABELING)
#         data = {
#             'text': 'example',
#             'task_type': 'Span'
#         }
#         serializer = LabelSerializer(data=data)
#         serializer.is_valid()
#         label = serializer.save(project=project.item)
#         created = Label.objects.get(pk=label.id)
#         self.assertEqual(label, created)
