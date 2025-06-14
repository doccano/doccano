from django.contrib import admin

from .models import AutoLabelingConfig


class AutoLabelingConfigAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "model_name",
        "model_attrs",
    )
    ordering = ("project",)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["model_name"]
        else:
            return []


admin.site.register(AutoLabelingConfig, AutoLabelingConfigAdmin)
