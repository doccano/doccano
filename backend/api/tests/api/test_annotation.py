from rest_framework import status
from rest_framework.reverse import reverse

from api.models import (DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING,
                        Category, Span, TextLabel)

from .utils import (CRUDMixin, make_annotation, make_doc, make_label,
                    make_user, prepare_project)


class TestAnnotationList:
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = 'annotation_list'

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(task=cls.task)
        cls.non_member = make_user()
        doc = make_doc(cls.project.item)
        for member in cls.project.users:
            cls.make_annotation(doc, member)
        cls.url = reverse(viewname=cls.view_name, args=[cls.project.item.id, doc.id])

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member)

    def test_allows_project_member_to_fetch_annotation(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)  # fetch only own annotation

    def test_denies_non_project_member_to_fetch_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_fetch_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_bulk_delete_annotation(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)
        count = self.model.objects.count()
        self.assertEqual(count, 2)  # delete only own annotation


class TestCategoryList(TestAnnotationList, CRUDMixin):
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = 'category_list'


class TestSpanList(TestAnnotationList, CRUDMixin):
    model = Span
    task = SEQUENCE_LABELING
    view_name = 'span_list'

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member, start_offset=0, end_offset=1)


class TestTextList(TestAnnotationList, CRUDMixin):
    model = TextLabel
    task = SEQ2SEQ
    view_name = 'text_list'


class TestSharedAnnotationList:
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = 'annotation_list'

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(task=cls.task, collaborative_annotation=True)
        doc = make_doc(cls.project.item)
        for member in cls.project.users:
            cls.make_annotation(doc, member)
        cls.url = reverse(viewname=cls.view_name, args=[cls.project.item.id, doc.id])

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member)

    def test_allows_project_member_to_fetch_all_annotation(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 3)

    def test_allows_project_member_to_bulk_delete_annotation(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)
        count = self.model.objects.count()
        self.assertEqual(count, 0)  # delete all annotation in the doc


class TestSharedCategoryList(TestSharedAnnotationList, CRUDMixin):
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = 'category_list'


class TestSharedSpanList(TestSharedAnnotationList, CRUDMixin):
    model = Span
    task = SEQUENCE_LABELING
    view_name = 'span_list'
    start_offset = 0

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(
            cls.task,
            doc=doc,
            user=member,
            start_offset=cls.start_offset,
            end_offset=cls.start_offset + 1
        )
        cls.start_offset += 1


class TestSharedTextList(TestSharedAnnotationList, CRUDMixin):
    model = TextLabel
    task = SEQ2SEQ
    view_name = 'text_list'


class TestAnnotationCreation:
    task = DOCUMENT_CLASSIFICATION
    view_name = 'annotation_list'

    def setUp(self):
        self.project = prepare_project(task=self.task)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        self.data = self.create_data()
        self.url = reverse(viewname=self.view_name, args=[self.project.item.id, doc.id])

    def create_data(self):
        label = make_label(self.project.item)
        return {'label': label.id}

    def test_allows_project_member_to_annotate(self):
        for member in self.project.users:
            self.assert_create(member, status.HTTP_201_CREATED)

    def test_denies_non_project_member_to_annotate(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_annotate(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestCategoryCreation(TestAnnotationCreation, CRUDMixin):
    view_name = 'category_list'


class TestSpanCreation(TestAnnotationCreation, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = 'span_list'

    def create_data(self):
        label = make_label(self.project.item)
        return {'label': label.id, 'start_offset': 0, 'end_offset': 1}


class TestTextLabelCreation(TestAnnotationCreation, CRUDMixin):
    task = SEQ2SEQ
    view_name = 'text_list'

    def create_data(self):
        return {'text': 'example'}


class TestAnnotationDetail:
    task = SEQUENCE_LABELING
    view_name = 'annotation_detail'

    def setUp(self):
        self.project = prepare_project(task=self.task)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        label = make_label(self.project.item)
        annotation = self.create_annotation_data(doc=doc)
        self.data = {'label': label.id}
        self.url = reverse(viewname=self.view_name, args=[self.project.item.id, doc.id, annotation.id])

    def create_annotation_data(self, doc):
        return make_annotation(
            task=self.task,
            doc=doc,
            user=self.project.users[0],
            start_offset=0,
            end_offset=1
        )

    def test_allows_owner_to_get_annotation(self):
        self.assert_fetch(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_owner_to_get_annotation(self):
        for member in self.project.users[1:]:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_get_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_annotation(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_owner_to_update_annotation(self):
        self.assert_update(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_owner_to_update_annotation(self):
        for member in self.project.users[1:]:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_annotation(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_owner_to_delete_annotation(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)

    def test_denies_non_owner_to_delete_annotation(self):
        for member in self.project.users[1:]:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_annotation(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)


class TestCategoryDetail(TestAnnotationDetail, CRUDMixin):
    task = DOCUMENT_CLASSIFICATION
    view_name = 'category_detail'

    def create_annotation_data(self, doc):
        return make_annotation(task=self.task, doc=doc, user=self.project.users[0])


class TestSpanDetail(TestAnnotationDetail, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = 'span_detail'


class TestTextDetail(TestAnnotationDetail, CRUDMixin):
    task = SEQ2SEQ
    view_name = 'text_detail'

    def setUp(self):
        super().setUp()
        self.data = {'text': 'changed'}

    def create_annotation_data(self, doc):
        return make_annotation(task=self.task, doc=doc, user=self.project.users[0])


class TestSharedAnnotationDetail:
    task = DOCUMENT_CLASSIFICATION
    view_name = 'annotation_detail'

    def setUp(self):
        self.project = prepare_project(task=self.task, collaborative_annotation=True)
        doc = make_doc(self.project.item)
        annotation = self.make_annotation(doc, self.project.users[0])
        label = make_label(self.project.item)
        self.data = {'label': label.id}
        self.url = reverse(viewname=self.view_name, args=[self.project.item.id, doc.id, annotation.id])

    def make_annotation(self, doc, member):
        return make_annotation(self.task, doc=doc, user=member)

    def test_allows_any_member_to_get_annotation(self):
        for member in self.project.users:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_allows_any_member_to_update_annotation(self):
        for member in self.project.users:
            self.assert_update(member, status.HTTP_200_OK)

    def test_allows_any_member_to_delete_annotation(self):
        self.assert_delete(self.project.users[1], status.HTTP_204_NO_CONTENT)


class TestSharedCategoryDetail(TestSharedAnnotationDetail, CRUDMixin):
    view_name = 'category_detail'


class TestSharedSpanDetail(TestSharedAnnotationDetail, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = 'span_detail'

    def make_annotation(self, doc, member):
        return make_annotation(self.task, doc=doc, user=member, start_offset=0, end_offset=1)


class TestSharedTextDetail(TestSharedAnnotationDetail, CRUDMixin):
    task = SEQ2SEQ
    view_name = 'text_detail'

    def setUp(self):
        super().setUp()
        self.data = {'text': 'changed'}
