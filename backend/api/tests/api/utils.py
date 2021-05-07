import os
from collections import namedtuple
from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from model_mommy import mommy

from ...models import (DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING,
                       SPEECH2TEXT, Role, RoleMapping)

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')


ProjectData = namedtuple('ProjectData', ['item', 'users'])


def create_default_roles():
    Role.objects.get_or_create(name=settings.ROLE_PROJECT_ADMIN)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATOR)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATION_APPROVER)


def assign_user_to_role(project_member, project, role_name):
    role, _ = Role.objects.get_or_create(name=role_name)
    if RoleMapping.objects.filter(user=project_member, project=project).exists():
        mapping = RoleMapping.objects.get(user=project_member, project=project)
        mapping.role = role
        mapping.save()
    else:
        mapping = RoleMapping.objects.get_or_create(role_id=role.id, user_id=project_member.id, project_id=project.id)
    return mapping


def remove_all_role_mappings():
    RoleMapping.objects.all().delete()


def make_user(username: str):
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(username=username, password='pass')
    return user


def make_project(
        task: str,
        users: List[str],
        roles: List[str] = None):
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
        SPEECH2TEXT: 'Speech2TextProject'
    }[task]
    project = mommy.make(
        _model=project_model,
        project_type=task,
        users=users
    )

    # assign roles to the users.
    for user, role in zip(users, roles):
        assign_user_to_role(user, project, role)

    return ProjectData(
        item=project,
        users=users,
    )


def make_tag(project):
    return mommy.make('Tag', project=project)


class TestUtilsMixin:
    def _patch_project(self, project, attribute, value):
        old_value = getattr(project, attribute, None)
        setattr(project, attribute, value)
        project.save()

        def cleanup_project():
            setattr(project, attribute, old_value)
            project.save()

        self.addCleanup(cleanup_project)
