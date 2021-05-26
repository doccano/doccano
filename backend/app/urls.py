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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib.auth.views import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# TODO: adds AnnotationList and AnnotationDetail endpoint.
schema_view = get_schema_view(
   openapi.Info(
      title="doccano API",
      default_version='v1',
      description="doccano API description",
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = []
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('', TemplateView.as_view(template_name='index.html')),
]

if 'cloud_browser' in settings.INSTALLED_APPS:
    urlpatterns.append(path('cloud-storage/', include('cloud_browser.urls')))
