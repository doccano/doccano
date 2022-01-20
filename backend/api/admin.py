from django.contrib import admin

from .models import (Category, CategoryType, Comment, Example, Project,
                     Seq2seqProject, SequenceLabelingProject, Span, SpanType,
                     Tag, TextClassificationProject, TextLabel)


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


class SpanAdmin(admin.ModelAdmin):
    list_display = ('example', 'label', 'start_offset', 'user')
    ordering = ('example',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('example', 'label', 'user')
    ordering = ('example',)


class TextLabelAdmin(admin.ModelAdmin):
    list_display = ('example', 'text', 'user')
    ordering = ('example',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('project', 'text', )
    ordering = ('project', 'text', )
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'example', 'text', 'created_at', )
    ordering = ('user', 'created_at', )
    search_fields = ('user',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Span, SpanAdmin)
admin.site.register(TextLabel, TextLabelAdmin)
admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(SpanType, SpanTypeAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TextClassificationProject, ProjectAdmin)
admin.site.register(SequenceLabelingProject, ProjectAdmin)
admin.site.register(Seq2seqProject, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
