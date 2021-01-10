import sys
import logging
sys.path.append('../api')

from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from api.permissions import ProjectAdminMixin
from api.models import Project, RoleMapping
from app import settings

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'annotation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context['is_project_admin'] = RoleMapping.objects.filter(
            role_id__name=settings.ROLE_PROJECT_ADMIN,
            project=project.id,
            user=self.request.user.id
        ).exists()
        context['bundle_name'] = project.get_bundle_name()
        return context


class ProjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'projects.html'


class DatasetView(ProjectAdminMixin, LoginRequiredMixin, ListView):
    template_name = 'dataset.html'
    paginate_by = 5
    extra_context = {
        'bundle_name': 'dataset'
    }

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.documents.all()


class LabelView(ProjectAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin.html'
    extra_context = {
        'bundle_name': 'label'
    }


class StatsView(ProjectAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin.html'
    extra_context = {
        'bundle_name': 'stats'
    }


class GuidelineView(ProjectAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin.html'
    extra_context = {
        'bundle_name': 'guideline'
    }


class UsersView(ProjectAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin.html'
    extra_context = {
        'bundle_name': 'users'
    }


class DataUpload(ProjectAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context['bundle_name'] = project.get_bundle_name_upload()
        return context


class DataDownload(ProjectAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        context['bundle_name'] = project.get_bundle_name_download()
        return context


class LoginView(BaseLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    extra_context = {
        'github_login': bool(settings.SOCIAL_AUTH_GITHUB_KEY),
        'aad_login': bool(settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID),
        'okta_oauth_login': bool(settings.SOCIAL_AUTH_OKTA_OAUTH2_KEY),
        'okta_openidconnect_login': bool(settings.SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY),
        'allow_signup': bool(settings.ALLOW_SIGNUP),
    }

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['social_login_enabled'] = any(value for key, value in context.items()
                                              if key.endswith('_login'))
        return context


class DemoTextClassification(TemplateView):
    template_name = 'annotation.html'
    extra_context = {
        'bundle_name': 'demo_text_classification',
    }


class DemoNamedEntityRecognition(TemplateView):
    template_name = 'annotation.html'
    extra_context = {
        'bundle_name': 'demo_named_entity',
    }


class DemoTranslation(TemplateView):
    template_name = 'annotation.html'
    extra_context = {
        'bundle_name': 'demo_translation',
    }
