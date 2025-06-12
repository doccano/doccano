from django.urls import path

from .views import TaskStatus, DatabaseHealthCheck

urlpatterns = [
    path(route="tasks/status/<task_id>", view=TaskStatus.as_view(), name="task_status"),
    path(route="database/health", view=DatabaseHealthCheck.as_view(), name="database_health"),
]
