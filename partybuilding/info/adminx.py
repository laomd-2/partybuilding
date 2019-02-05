import xadmin
from django.http import HttpResponseRedirect
from .models import Member
from .resources import MemberResource


class MemberAdmin(object):
    import_export_args = {'import_resource_class': MemberResource}

    list_display = [field.name for field in Member._meta.get_fields()][1:]
    list_editable = list_display[1:]
    search_fields = ['name']
    list_filter = ['name']
    model_icon = 'fa fa-info'
    list_per_page = 15

    def queryset(self):
        if not self.request.user.is_superuser:  # 判断是否是超级用户
            member = Member.objects.get(netid=self.request.user)
            if self.request.user.has_perm('info.add_member'):   # 支书
                return self.model.objects.filter(branch_name=member.branch_name)
            return self.model.objects.filter(netid=member.netid, branch_name=member.branch_name)    # 普通成员
        return self.model.objects.all()


xadmin.site.register(Member, MemberAdmin)