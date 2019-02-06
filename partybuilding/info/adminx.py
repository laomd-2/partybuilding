import xadmin
from xadmin.layout import Main, TabHolder, Tab, Row, Fieldset
from .models import Member
from .resources import MemberResource


def take_every(alist, step=1):
    end = len(alist)
    for i in range(0, end, step):
        if i < end - 1:
            yield alist[i], alist[i + 1]
        else:
            yield alist[i]


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
            member = Member.objects.get(netid=self.request.user)
            if self.request.user.has_perm('info.add_member'):   # 支书
                return self.model.objects.filter(branch_name=member.branch_name)
            return self.model.objects.filter(netid=member.netid, branch_name=member.branch_name)    # 普通成员
        return self.model.objects.all()


xadmin.site.register(Member, MemberAdmin)
