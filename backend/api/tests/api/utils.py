from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import (DOCUMENT_CLASSIFICATION, IMAGE_CLASSIFICATION,
                             INTENT_DETECTION_AND_SLOT_FILLING, SEQ2SEQ,
                             SEQUENCE_LABELING, SPEECH2TEXT, Member)
from roles.models import Role


class ProjectData:

    def __init__(self, item, members):
        self.item = item
        self.members = members

    @property
    def admin(self):
        return self.members[0]

    @property
    def approver(self):
        return self.members[1]

    @property
    def annotator(self):
        return self.members[2]

    @property
    def staffs(self):
        return [self.approver, self.annotator]


def create_default_roles():
    Role.objects.get_or_create(name=settings.ROLE_PROJECT_ADMIN)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATOR)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATION_APPROVER)


def assign_user_to_role(project_member, project, role_name):
    role, _ = Role.objects.get_or_create(name=role_name)
    if Member.objects.filter(user=project_member, project=project).exists():
        mapping = Member.objects.get(user=project_member, project=project)
        mapping.role = role
        mapping.save()
    else:
        mapping = Member.objects.get_or_create(role_id=role.id, user_id=project_member.id, project_id=project.id)
    return mapping


def make_user(username: str = 'bob'):
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(username=username, password='pass')
    return user


def make_project(
        task: str,
        users: List[str],
        roles: List[str] = None,
        collaborative_annotation=False,
        **kwargs):
    create_default_roles()

    # create users.
    users = [
        make_user(name) for name in users
    ]

    # create a project.
    project_model = {
        DOCUMENT_CLASSIFICATION: 'TextClassificationProject',
        SEQUENCE_LABELING: 'SequenceLabelingProject',
        SEQ2SEQ: 'Seq2seqProject',
        SPEECH2TEXT: 'Speech2TextProject',
        IMAGE_CLASSIFICATION: 'ImageClassificationProject',
        INTENT_DETECTION_AND_SLOT_FILLING: 'IntentDetectionAndSlotFillingProject'
    }.get(task, 'Project')
    project = mommy.make(
        _model=project_model,
        project_type=task,
        collaborative_annotation=collaborative_annotation,
        created_by=users[0],
        **kwargs
    )

    # assign roles to the users.
    for user, role in zip(users, roles):
        assign_user_to_role(user, project, role)

    return ProjectData(
        item=project,
        members=users
    )


def make_tag(project):
    return mommy.make('Tag', project=project)


def prepare_project(task: str = 'Any', collaborative_annotation=False, **kwargs):
    return make_project(
        task=task,
        users=['admin', 'approver', 'annotator'],
        roles=[
            settings.ROLE_PROJECT_ADMIN,
            settings.ROLE_ANNOTATION_APPROVER,
            settings.ROLE_ANNOTATOR,
        ],
        collaborative_annotation=collaborative_annotation,
        **kwargs
    )


class CRUDMixin(APITestCase):
    url = ''
    data = {}

    def assert_fetch(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, expected)
        return response

    def assert_create(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, expected)
        return response

    def assert_update(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.patch(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, expected)
        return response

    def assert_delete(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, expected)
