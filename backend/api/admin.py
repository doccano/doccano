from django.contrib import admin

from .models import (Category, Comment, Example, Label, Project, Role,
                     RoleMapping, Seq2seqProject, SequenceLabelingProject,
                     Span, Tag, TextClassificationProject, TextLabel)


class LabelAdmin(admin.ModelAdmin):
    list_display = ('text', 'project', 'text_color', 'background_color')
    ordering = ('project',)
    search_fields = ('text',)


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


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ('name',)


class RoleMappingAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'project', )
    ordering = ('user',)
    search_fields = ('user__username',)


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
admin.site.register(Label, LabelAdmin)
admin.site.register(Example, ExampleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TextClassificationProject, ProjectAdmin)
admin.site.register(SequenceLabelingProject, ProjectAdmin)
admin.site.register(Seq2seqProject, ProjectAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleMapping, RoleMappingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
