from django.contrib import admin

from .models import Category, Span, TextLabel


class SpanAdmin(admin.ModelAdmin):
    list_display = ("example", "label", "start_offset", "user")
    ordering = ("example",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("example", "label", "user")
    ordering = ("example",)


class TextLabelAdmin(admin.ModelAdmin):
    list_display = ("example", "text", "user")
    ordering = ("example",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Span, SpanAdmin)
admin.site.register(TextLabel, TextLabelAdmin)
