from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from .utils import make_annotation
from api.tests.utils import CRUDMixin
from examples.tests.utils import make_doc
from label_types.tests.utils import make_label
from labels.models import Category, Span, TextLabel
from projects.models import DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING
from projects.tests.utils import prepare_project
from users.tests.utils import make_user


class TestLabelList:
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = "annotation_list"

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(task=cls.task)
        cls.non_member = make_user()
        doc = make_doc(cls.project.item)
        for member in cls.project.members:
            cls.make_annotation(doc, member)
        cls.url = reverse(viewname=cls.view_name, args=[cls.project.item.id, doc.id])

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member)

    def test_allows_project_member_to_fetch_annotation(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)  # fetch only own annotation

    def test_denies_non_project_member_to_fetch_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_fetch_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_bulk_delete_annotation(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)
        count = self.model.objects.count()
        self.assertEqual(count, 2)  # delete only own annotation


class TestCategoryList(TestLabelList, CRUDMixin):
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = "category_list"


class TestSpanList(TestLabelList, CRUDMixin):
    model = Span
    task = SEQUENCE_LABELING
    view_name = "span_list"

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member, start_offset=0, end_offset=1)


class TestTextList(TestLabelList, CRUDMixin):
    model = TextLabel
    task = SEQ2SEQ
    view_name = "text_list"


class TestSharedLabelList:
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = "annotation_list"

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(task=cls.task, collaborative_annotation=True)
        doc = make_doc(cls.project.item)
        for member in cls.project.members:
            cls.make_annotation(doc, member)
        cls.url = reverse(viewname=cls.view_name, args=[cls.project.item.id, doc.id])

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member)

    def test_allows_project_member_to_fetch_all_annotation(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 3)

    def test_allows_project_member_to_bulk_delete_annotation(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)
        count = self.model.objects.count()
        self.assertEqual(count, 0)  # delete all annotation in the doc


class TestSharedCategoryList(TestSharedLabelList, CRUDMixin):
    model = Category
    task = DOCUMENT_CLASSIFICATION
    view_name = "category_list"


class TestSharedSpanList(TestSharedLabelList, CRUDMixin):
    model = Span
    task = SEQUENCE_LABELING
    view_name = "span_list"
    start_offset = 0

    @classmethod
    def make_annotation(cls, doc, member):
        make_annotation(cls.task, doc=doc, user=member, start_offset=cls.start_offset, end_offset=cls.start_offset + 1)
        cls.start_offset += 1


class TestSharedTextList(TestSharedLabelList, CRUDMixin):
    model = TextLabel
    task = SEQ2SEQ
    view_name = "text_list"


class TestDataLabeling:
    task = DOCUMENT_CLASSIFICATION
    view_name = "annotation_list"

    def setUp(self):
        self.project = prepare_project(task=self.task)
        self.non_member = make_user()
        self.doc = make_doc(self.project.item)
        self.data = self.create_data()
        self.url = reverse(viewname=self.view_name, args=[self.project.item.id, self.doc.id])

    def create_data(self):
        label = make_label(self.project.item)
        return {"label": label.id}

    def test_allows_project_member_to_annotate(self):
        for member in self.project.members:
            self.assert_create(member, status.HTTP_201_CREATED)

    def test_denies_non_project_member_to_annotate(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_annotate(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestCategoryCreation(TestDataLabeling, CRUDMixin):
    view_name = "category_list"


class TestSpanCreation(TestDataLabeling, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = "span_list"

    def create_data(self):
        label = make_label(self.project.item)
        return {"label": label.id, "start_offset": 0, "end_offset": 1}


class TestRelationCreation(TestDataLabeling, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = "relation_list"

    def create_data(self):
        relation_type = mommy.make("RelationType", project=self.project.item)
        from_id = mommy.make("Span", example=self.doc, start_offset=0, end_offset=1)
        to_id = mommy.make("Span", example=self.doc, start_offset=1, end_offset=2)
        return {"type": relation_type.id, "from_id": from_id.id, "to_id": to_id.id}


class TestTextLabelCreation(TestDataLabeling, CRUDMixin):
    task = SEQ2SEQ
    view_name = "text_list"

    def create_data(self):
        return {"text": "example"}


class TestLabelDetail:
    task = SEQUENCE_LABELING
    view_name = "annotation_detail"

    def setUp(self):
        self.project = prepare_project(task=self.task)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        label = make_label(self.project.item)
        annotation = self.create_annotation_data(doc=doc)
        self.data = {"label": label.id}
        self.url = reverse(viewname=self.view_name, args=[self.project.item.id, doc.id, annotation.id])

    def create_annotation_data(self, doc):
        return make_annotation(task=self.task, doc=doc, user=self.project.admin, start_offset=0, end_offset=1)

    def test_allows_owner_to_get_annotation(self):
        self.assert_fetch(self.project.admin, status.HTTP_200_OK)

    def test_denies_non_owner_to_get_annotation(self):
        for member in self.project.staffs:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_get_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_annotation(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_owner_to_update_annotation(self):
        self.assert_update(self.project.admin, status.HTTP_200_OK)

    def test_denies_non_owner_to_update_annotation(self):
        for member in self.project.staffs:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_annotation(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_owner_to_delete_annotation(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)

    def test_denies_non_owner_to_delete_annotation(self):
        for member in self.project.staffs:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_annotation(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)


class TestCategoryDetail(TestLabelDetail, CRUDMixin):
    task = DOCUMENT_CLASSIFICATION
    view_name = "category_detail"

    def create_annotation_data(self, doc):
        return make_annotation(task=self.task, doc=doc, user=self.project.admin)


class TestSpanDetail(TestLabelDetail, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = "span_detail"


class TestTextDetail(TestLabelDetail, CRUDMixin):
    task = SEQ2SEQ
    view_name = "text_detail"

    def setUp(self):
        super().setUp()
        self.data = {"text": "changed"}

    def create_annotation_data(self, doc):
        return make_annotation(task=self.task, doc=doc, user=self.project.admin)


class TestSharedLabelDetail:
    task = DOCUMENT_CLASSIFICATION
    view_name = "annotation_detail"

    def setUp(self):
        self.project = prepare_project(task=self.task, collaborative_annotation=True)
        doc = make_doc(self.project.item)
        annotation = self.make_annotation(doc, self.project.admin)
        label = make_label(self.project.item)
        self.data = {"label": label.id}
        self.url = reverse(viewname=self.view_name, args=[self.project.item.id, doc.id, annotation.id])

    def make_annotation(self, doc, member):
        return make_annotation(self.task, doc=doc, user=member)

    def test_allows_any_member_to_get_annotation(self):
        for member in self.project.members:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_allows_any_member_to_update_annotation(self):
        for member in self.project.members:
            self.assert_update(member, status.HTTP_200_OK)

    def test_allows_any_member_to_delete_annotation(self):
        self.assert_delete(self.project.approver, status.HTTP_204_NO_CONTENT)


class TestSharedCategoryDetail(TestSharedLabelDetail, CRUDMixin):
    view_name = "category_detail"


class TestSharedSpanDetail(TestSharedLabelDetail, CRUDMixin):
    task = SEQUENCE_LABELING
    view_name = "span_detail"

    def make_annotation(self, doc, member):
        return make_annotation(self.task, doc=doc, user=member, start_offset=0, end_offset=1)


class TestSharedTextDetail(TestSharedLabelDetail, CRUDMixin):
    task = SEQ2SEQ
    view_name = "text_detail"

    def setUp(self):
        super().setUp()
        self.data = {"text": "changed"}
