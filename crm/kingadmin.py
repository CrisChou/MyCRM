from kingadmin.sites import site
from kingadmin.admin_base import BaseKingAdmin
from crm import models


class CustomerAdmin(BaseKingAdmin):
    list_display = [
        'name', 'source', 'contact_type', 'contact', 'consultant',
        'consult_content', 'status', 'date'
    ]
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = [
        'name',
    ]
    readonly_fields = [
        'status',
    ]
    filter_horizontal = [
        'consult_courses',
    ]


site.register(models.CustomerInfo, CustomerAdmin)
site.register(models.Role)
site.register(models.CustomerFollowUp)
site.register(models.ContractTemplate)
site.register(models.Menus)
