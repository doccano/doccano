from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, ProjectQuestionStatsView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('projects/<int:project_id>/perspective/', include(router.urls)),
    path('projects/<int:project_id>/perspective/stats/', ProjectQuestionStatsView.as_view(), name='perspective-stats'),
]
