from django.contrib import admin

from .models import (Project, Seq2seqProject, SequenceLabelingProject, Tag,
                     TextClassificationProject)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project_type', 'random_order', 'collaborative_annotation')
    ordering = ('project_type',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('project', 'text', )
    ordering = ('project', 'text', )
    search_fields = ('text',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(TextClassificationProject, ProjectAdmin)
admin.site.register(SequenceLabelingProject, ProjectAdmin)
admin.site.register(Seq2seqProject, ProjectAdmin)
admin.site.register(Tag, TagAdmin)
