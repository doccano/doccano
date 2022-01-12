from django.contrib import admin

from .models import Role, Member


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ('name',)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'project', )
    ordering = ('user',)
    search_fields = ('user__username',)


admin.site.register(Role, RoleAdmin)
admin.site.register(Member, MemberAdmin)
