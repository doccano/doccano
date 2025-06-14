from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.utils import CRUDMixin
from examples.tests.utils import make_doc
from label_types.tests.utils import make_label
from projects.models import Member, Project, ProjectType
from projects.tests.utils import prepare_project
from roles.tests.utils import create_default_roles
from users.tests.utils import make_user


class TestProjectList(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project()
        cls.non_member = make_user()
        cls.url = reverse(viewname="project_list")

    def test_return_projects_to_member(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            project = response.data["results"][0]
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(project["id"], self.project.item.id)

    def test_does_not_return_project_to_non_member(self):
        response = self.assert_fetch(self.non_member, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class TestProjectCreate(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        create_default_roles()
        cls.user = make_user()
        cls.url = reverse(viewname="project_list")
        cls.data = {
            "name": "example",
            "project_type": "DocumentClassification",
            "description": "example",
            "guideline": "example",
            "resourcetype": "TextClassificationProject",
        }

    def test_allows_staff_user_to_create_project(self):
        self.user.is_staff = True
        self.user.save()
        response = self.assert_create(self.user, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.data["name"])

    def test_exists_project_administrator(self):
        self.user.is_staff = True
        self.user.save()
        response = self.assert_create(self.user, status.HTTP_201_CREATED)
        members = Member.objects.filter(project=response.data["id"])
        self.assertEqual(members.count(), 1)
        member = members.first()
        self.assertEqual(member.role.name, settings.ROLE_PROJECT_ADMIN)

    def test_denies_non_staff_user_to_create_project(self):
        self.assert_create(self.user, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_create_project(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestSequenceLabelingProjectCreation(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        create_default_roles()
        cls.user = make_user()
        cls.url = reverse(viewname="project_list")
        cls.data = {
            "name": "example",
            "project_type": "SequenceLabeling",
            "description": "example",
            "guideline": "example",
            "allow_overlapping": True,
            "grapheme_mode": True,
            "resourcetype": "SequenceLabelingProject",
        }

    def test_allows_staff_user_to_create_project(self):
        self.user.is_staff = True
        self.user.save()
        response = self.assert_create(self.user, status.HTTP_201_CREATED)
        self.assertEqual(response.data["allow_overlapping"], self.data["allow_overlapping"])
        self.assertEqual(response.data["grapheme_mode"], self.data["grapheme_mode"])


class TestProjectDetailAPI(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project("SequenceLabeling")
        cls.non_member = make_user()
        cls.url = reverse(viewname="project_detail", args=[cls.project.item.id])
        cls.data = {"description": "lorem", "resourcetype": "SequenceLabelingProject"}

    def test_return_project_to_member(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], self.project.item.id)

    def test_does_not_return_project_to_non_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_update_project(self):
        response = self.assert_update(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], self.data["description"])

    def test_denies_project_staff_to_update_project(self):
        for member in self.project.staffs:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_member_to_update_project(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_delete_project(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)

    def test_denies_project_staff_to_delete_project(self):
        for member in self.project.staffs:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_member_to_delete_project(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)


class TestProjectModel(TestCase):
    def setUp(self):
        self.project = prepare_project().item

    def test_clone_project(self):
        project = self.project.clone()
        self.assertNotEqual(project.id, self.project.id)
        self.assertEqual(project.name, self.project.name)
        self.assertEqual(project.role_mappings.count(), self.project.role_mappings.count())


class TestCloneProject(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        cls.project = project.item
        cls.user = project.admin
        make_doc(cls.project)
        cls.category_type = make_label(cls.project)
        cls.url = reverse(viewname="clone_project", args=[cls.project.id])

    def test_clone_project(self):
        response = self.assert_create(self.user, status.HTTP_201_CREATED)

        project = Project.objects.get(id=response.data["id"])

        # assert project
        self.assertNotEqual(project.id, self.project.id)
        self.assertEqual(project.name, self.project.name)

        # assert category type
        category_type = project.categorytype_set.first()
        self.assertEqual(category_type.text, self.category_type.text)

        # assert example
        example = self.project.examples.first()
        cloned_example = project.examples.first()
        self.assertEqual(example.text, cloned_example.text)
