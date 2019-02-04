import xadmin
from .models import Member
from .resources import MemberResource


class MemberAdmin(object):
    import_export_args = {'import_resource_class': MemberResource}

    list_display = [field.name for field in Member._meta.get_fields()][1:]
    list_editable = list_display[1:]
    search_fields = ['name']
    list_filter = ['name']
    model_icon = 'fa fa-info'


xadmin.site.register(Member, MemberAdmin)
