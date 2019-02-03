import xadmin
from .models import Member


class MemberAdmin(object):
    list_display = ['netid', 'name', 'application_date']
    search_fields = ['netid']
    list_editable = ['netid', 'name', 'application_date']
    list_filter = ['netid']


xadmin.site.register(Member, MemberAdmin)
