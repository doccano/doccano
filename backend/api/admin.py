from django.contrib import admin

from .models import (CategoryType, Comment, Example, Project, Seq2seqProject,
                     SequenceLabelingProject, SpanType, Tag,
                     TextClassificationProject)


class LabelAdmin(admin.ModelAdmin):
    list_display = ('text', 'project', 'text_color', 'background_color')
    ordering = ('project',)
    search_fields = ('text',)


class CategoryTypeAdmin(LabelAdmin):
    pass


class SpanTypeAdmin(LabelAdmin):
    pass


class ExampleAdmin(admin.ModelAdmin):
    list_display = ('text', 'project', 'meta')
    ordering = ('project',)
    search_fields = ('text',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project_type', 'random_order', 'collaborative_annotation')
    ordering = ('project_type',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('project', 'text', )
    ordering = ('project', 'text', )
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'example', 'text', 'created_at', )
    ordering = ('user', 'created_at', )
    search_fields = ('user',)


admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(SpanType, SpanTypeAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TextClassificationProject, ProjectAdmin)
admin.site.register(SequenceLabelingProject, ProjectAdmin)
admin.site.register(Seq2seqProject, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
