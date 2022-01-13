from django.contrib import admin

from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'project', )
    ordering = ('user',)
    search_fields = ('user__username',)


admin.site.register(Member, MemberAdmin)
