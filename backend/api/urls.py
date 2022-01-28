from django.urls import include, path

from .views import project, tag, task

urlpatterns_project = [
    path(
        route='tags',
        view=tag.TagList.as_view(),
        name='tag_list'
    ),
    path(
        route='tags/<int:tag_id>',
        view=tag.TagDetail.as_view(),
        name='tag_detail'
    ),
]

urlpatterns = [
    path(
        route='projects',
        view=project.ProjectList.as_view(),
        name='project_list'
    ),
    path(
        route='tasks/status/<task_id>',
        view=task.TaskStatus.as_view(),
        name='task_status'
    ),
    path(
        route='projects/<int:project_id>',
        view=project.ProjectDetail.as_view(),
        name='project_detail'
    ),
    path('projects/<int:project_id>/', include(urlpatterns_project))
]
