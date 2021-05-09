from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver

from .models import Project, Role, RoleMapping


@receiver(post_save, sender=RoleMapping)
def add_linked_project(sender, instance, created, **kwargs):
    if not created:
        return
    userInstance = instance.user
    projectInstance = instance.project
    if userInstance and projectInstance:
        user = User.objects.get(pk=userInstance.pk)
        project = Project.objects.get(pk=projectInstance.pk)
        user.projects.add(project)
        user.save()


@receiver(m2m_changed, sender=Project.users.through)
def remove_mapping_on_remove_user_from_project(sender, instance, action, reverse, **kwargs):
    # if reverse is True, pk_set is project_ids and instance is user.
    # else, pk_set is user_ids and instance is project.
    user_ids = kwargs['pk_set']
    if action.startswith('post_remove') and not reverse:
        RoleMapping.objects.filter(user__in=user_ids, project=instance).delete()
    elif action.startswith('post_add') and not reverse:
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        RoleMapping.objects.bulk_create(
            [RoleMapping(role=admin_role, project=instance, user_id=user)
             for user in user_ids
             if not RoleMapping.objects.filter(project=instance, user_id=user).exists()]
        )


@receiver(pre_delete, sender=RoleMapping)
def delete_linked_project(sender, instance, using, **kwargs):
    userInstance = instance.user
    projectInstance = instance.project
    if userInstance and projectInstance:
        user = User.objects.get(pk=userInstance.pk)
        project = Project.objects.get(pk=projectInstance.pk)
        user.projects.remove(project)
        user.save()
