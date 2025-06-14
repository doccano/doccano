from django.contrib import admin

from .models import CategoryType, SpanType


class LabelAdmin(admin.ModelAdmin):
    list_display = ("text", "project", "text_color", "background_color")
    ordering = ("project",)
    search_fields = ("text",)


class CategoryTypeAdmin(LabelAdmin):
    pass


class SpanTypeAdmin(LabelAdmin):
    pass


admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(SpanType, SpanTypeAdmin)
