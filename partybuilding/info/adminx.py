import xadmin
from .models import Member


class MemberAdmin(object):
    list_display = ['username', 'name', 'application_date']
    search_fields = ['name']
    list_editable = ['application_date']
    list_filter = ['name']


xadmin.site.register(Member, MemberAdmin)
