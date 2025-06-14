from django.contrib import admin

from .models import Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    ordering = ("name",)
    search_fields = ("name",)


admin.site.register(Role, RoleAdmin)
