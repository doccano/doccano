"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import re
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import TemplateView
from django.urls import include, path, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from label_types.views import CategoryTypeList, CategoryTypeDetail

schema_view = get_schema_view(
    openapi.Info(
        title="doccano API",
        default_version="v1",
        description="doccano API description",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = []
if settings.DEBUG or os.environ.get("STANDALONE", False):
    static_dir = Path(__file__).resolve().parent.parent / "client" / "dist"
    # For showing images and audios in the case of pip and Docker.
    urlpatterns.append(
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
            serve,
            {"document_root": settings.MEDIA_ROOT},
        )
    )
    # For showing favicon on the case of pip and Docker.
    urlpatterns.append(path("favicon.ico", serve, {"document_root": static_dir, "path": "favicon.ico"}))

urlpatterns += [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("social/", include("social.urls")),
    path("v1/social/", include("social.v1_urls")),
    path("v1/health/", include("health_check.urls")),
    path("v1/", include("api.urls")),
    path("v1/", include("roles.urls")),
    path("v1/", include("users.urls")),
    path("v1/", include("data_import.urls")),
    path("v1/", include("data_export.urls")),
    path("v1/", include("projects.urls")),
    path("v1/projects/<int:project_id>/metrics/", include("metrics.urls")),
    path("v1/projects/<int:project_id>/", include("auto_labeling.urls")),
    path("v1/projects/<int:project_id>/", include("examples.urls")),
    path("v1/projects/<int:project_id>/", include("labels.urls")),
    path("v1/projects/<int:project_id>/", include("label_types.urls")),
    path("v1/", include("perspectives.urls")),
    path('v1/annotations/', include('annotations.urls')),
    path("v1/projects/<int:project_id>/perspectives/", include("perspectives.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("v1/projects/<int:project_id>/category-types/", CategoryTypeList.as_view(), name="project_category_types"),
    path("v1/projects/<int:project_id>/category-types/<int:label_id>/", CategoryTypeDetail.as_view(), name="project_category_type"),
]
