from django.contrib import admin
from acapella.models import PermissionModel

class PermissionModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'user', 'permission')
    ordering = ('-model',)


admin.site.register(PermissionModel, PermissionModelAdmin)
