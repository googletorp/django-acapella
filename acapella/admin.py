from django.contrib import admin
from acapella.models import PermissionSlip

class PermissionSlipAdmin(admin.ModelAdmin):
    list_display = ('slip', 'user', 'permission')
    ordering = ('-slip',)


admin.site.register(PermissionSlip, PermissionSlipAdmin)
