from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_permission_codename
from django.db.models.options import Options

import xadmin
from xadmin.layout import Main, TabHolder, Tab, Row, Fieldset
from .models import Branch, Member
from .resources import MemberResource

ModelAdmin
@xadmin.sites.register(Branch)
class BranchAdmin(object):
    list_display = ['id', 'branch_name']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['branch_name']
    model_icon = 'fa fa-users'
    list_per_page = 15
    list_editable = list_display[1:]

    # def has_delete_permission(self, request=None, obj=None):
    #     if request is None:
    #         return False
    #     has = request.user.is_superuser
    #     print('def has_delete_permission', has)
    #     return has


@xadmin.sites.register(Member)
class MemberAdmin(object):
    import_export_args = {'import_resource_class': MemberResource}

    fields = [field.name for field in Member._meta.fields]
    list_display = fields[1:8]
    search_fields = ['name']
    list_filter = ['name', 'application_date',
                   'activist_date',
                   'key_develop_person_date',
                   'first_branch_conference',
                   'second_branch_conference']
    model_icon = 'fa fa-info'
    list_per_page = 10
    list_editable = list_display[1:]
    # relfield_style = 'fk_ajax'

    phases = dict()
    phases['基本信息'] = fields[:8]
    phases['阶段1：入党考察'] = fields[8:17]
    phases['阶段2：预备党员'] = fields[17:26]
    phases['阶段3：正式党员'] = fields[26:]
    wizard_form_list = phases.items()
    form_layout = (
        Main(
            *[Fieldset(k, *v) for k, v in wizard_form_list]
        )
    )

    def get_readonly_fields(self):
        if not self.request.user.has_perm('info.add_member'):  # 普通成员
            return ['branch_name', 'netid'] + self.fields[8:]
        return []

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是超级用户
            try:
                member = Member.objects.get(netid=self.request.user)
                if self.request.user.has_perm('info.add_member'):  # 支书
                    return self.model.objects.filter(branch=member.branch)
                return self.model.objects.filter(netid=member.netid, branch=member.branch)  # 普通成员
            except:
                return self.model.objects.filter(netid="")
        return self.model.objects.all()
