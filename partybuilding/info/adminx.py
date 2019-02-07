import xadmin
from xadmin.layout import Main, TabHolder, Tab, Row, Fieldset
from .models import Branch, Member
from .resources import MemberResource


@xadmin.sites.register(Branch)
class BranchAdmin(object):
    list_display = ['id', 'branch_name']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['branch_name']
    model_icon = 'fa fa-users'
    list_per_page = 15
    list_editable = list_display[1:]


@xadmin.sites.register(Member)
class MemberAdmin(object):
    import_export_args = {'import_resource_class': MemberResource}

    fields = [field.name for field in Member._meta.fields]
    list_display = fields[1:8]
    search_fields = ['name']
    list_filter = ['name']
    model_icon = 'fa fa-info'
    list_per_page = 15
    list_editable = list_display[1:]

    form_layout = (
        Main(
            # TabHolder(Tab('基本',
            Fieldset('基本信息', *fields[:8]),
            Fieldset('阶段1：入党考察', *fields[8:17]),
            Fieldset('阶段2：预备党员', *fields[17:26]),
            Fieldset('阶段3：正式党员', *fields[26:])
        )
    )

    def get_readonly_fields(self):
        if not self.request.user.has_perm('info.add_member'):  # 普通成员
            return ['branch_name', 'netid'] + self.fields[8:]
        return []

    def queryset(self):
        if not self.request.user.is_superuser:  # 判断是否是超级用户
            try:
                member = Member.objects.get(netid=self.request.user)
                if self.request.user.has_perm('info.add_member'):  # 支书
                    return self.model.objects.filter(branch=member.branch)
                return self.model.objects.filter(netid=member.netid, branch=member.branch)  # 普通成员
            except:
                return self.model.objects.filter(netid="")
        return self.model.objects.all()
