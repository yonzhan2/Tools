from django.contrib import admin
from vminfo.models import VCInfo, VMList


# Register your models here.
class VCInfoAdmin(admin.ModelAdmin):
    list_display = ['vcname']
    list_filter = ['vcname']


class VMListAdmin(admin.ModelAdmin):
    list_display = ['vcname', 'dcname', 'cluster', 'hostip', 'vmname', 'vmip', 'vmmacc', 'status', 'vmpath']
    search_fields = ['vmname', 'vmip']
    list_filter = ['vcname']


admin.site.register(VCInfo, VCInfoAdmin)
admin.site.register(VMList, VMListAdmin)
