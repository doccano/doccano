from django.urls import path, include

from .views.member import MemberDetail, MemberList, MyRole
from .views.project import (
    CloneProject,
    ProjectDetail,
    ProjectList,
    CloseProject,
    ReopenProject,
    ProjectVersionList,
    ProjectVersionStatus,
    DebugDiscrepancies,
    VersionsReport,
    VersionsReportExport,
    VersionsReportPDFExport,
    TestPDFExport,
    ProjectDebugStatus,
)
from .views.tag import TagDetail, TagList

urlpatterns = [
    path(route="projects", view=ProjectList.as_view(), name="project_list"),
    path(route="projects/<int:project_id>", view=ProjectDetail.as_view(), name="project_detail"),
    path(route="projects/<int:project_id>/my-role", view=MyRole.as_view(), name="my_role"),
    path(route="projects/<int:project_id>/tags", view=TagList.as_view(), name="tag_list"),
    path(route="projects/<int:project_id>/tags/<int:tag_id>", view=TagDetail.as_view(), name="tag_detail"),
    path(route="projects/<int:project_id>/members", view=MemberList.as_view(), name="member_list"),
    path(route="projects/<int:project_id>/clone", view=CloneProject.as_view(), name="clone_project"),
    path(route="projects/<int:project_id>/members/<int:member_id>", view=MemberDetail.as_view(), name="member_detail"),
    path(route="projects/<int:project_id>/close", view=CloseProject.as_view(), name="close_project"),
    path(route="projects/<int:project_id>/reopen", view=ReopenProject.as_view(), name="reopen_project"),
    path(route="projects/<int:project_id>/versions", view=ProjectVersionList.as_view(), name="project_versions"),
    path(route="projects/<int:project_id>/version-status", view=ProjectVersionStatus.as_view(), name="project_version_status"),
    path(route="projects/<int:project_id>/debug-discrepancies", view=DebugDiscrepancies.as_view(), name="debug_discrepancies"),
    path(route="projects/<int:project_id>/debug-status", view=ProjectDebugStatus.as_view(), name="debug_status"),
    path(route="projects/<int:project_id>/versions-report", view=VersionsReport.as_view(), name="versions_report"),
    path(route="projects/<int:project_id>/versions-report/export", view=VersionsReportExport.as_view(), name="versions_report_export"),
    path(route="projects/<int:project_id>/versions-report/export-pdf", view=VersionsReportPDFExport.as_view(), name="versions_report_export_pdf"),
    path(route="projects/<int:project_id>/test-pdf", view=TestPDFExport.as_view(), name="test_pdf"),
    path('', include('projects.perspective.urls')),
]
