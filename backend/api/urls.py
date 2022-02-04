from django.urls import path

from .views import task

urlpatterns = [
    path(
        route='tasks/status/<task_id>',
        view=task.TaskStatus.as_view(),
        name='task_status'
    ),
]
