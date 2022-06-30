from django.contrib import admin

from .models import BoundingBox, Category, Segmentation, Span, TextLabel


class SpanAdmin(admin.ModelAdmin):
    list_display = ("example", "label", "start_offset", "user")
    ordering = ("example",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("example", "label", "user")
    ordering = ("example",)


class TextLabelAdmin(admin.ModelAdmin):
    list_display = ("example", "text", "user")
    ordering = ("example",)


class BoundingBoxAdmin(admin.ModelAdmin):
    list_display = ("example", "label", "user", "x", "y", "width", "height")
    ordering = ("example",)


class SegmentationAdmin(admin.ModelAdmin):
    list_display = ("example", "label", "user", "points")
    ordering = ("example",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Span, SpanAdmin)
admin.site.register(TextLabel, TextLabelAdmin)
admin.site.register(BoundingBox, BoundingBoxAdmin)
admin.site.register(Segmentation, SegmentationAdmin)
