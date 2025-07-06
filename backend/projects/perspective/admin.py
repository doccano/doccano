from django.contrib import admin
from .models import Question, QuestionOption, Answer


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'project', 'question_type', 'is_required', 'order', 'created_at')
    list_filter = ('question_type', 'is_required', 'project')
    search_fields = ('text', 'project__name')
    ordering = ('project', 'order', 'created_at')
    inlines = [QuestionOptionInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'text_answer', 'selected_option', 'created_at')
    list_filter = ('question__project', 'question__question_type', 'created_at')
    search_fields = ('question__text', 'user__username', 'text_answer')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question', 'user', 'selected_option')
