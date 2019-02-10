from django.contrib import messages
import xadmin
from user.models import get_bind_member
from xadmin.layout import Main, Fieldset
from .models import School, Branch, Member
from .resources import MemberResource


@xadmin.sites.register(School)
class SchoolAdmin(object):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15
    list_editable = list_display[1:]


@xadmin.sites.register(Branch)
class BranchAdmin(object):
    list_display = ['id', 'branch_name']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['branch_name']
    model_icon = 'fa fa-user'
    list_per_page = 15
    list_editable = list_display[1:]


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
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            member = get_bind_member(self.request.user)
            if member is None:
                return self.model.objects.none()
            else:
                if self.request.user.has_perm('info.add_member'):  # 支书
                    return self.model.objects.filter(branch=member.branch)
                return self.model.objects.filter(netid=member.netid, branch=member.branch)  # 普通成员
        return self.model.objects.all()

    def save_models(self):
        if hasattr(self, 'new_obj'):
            obj = self.new_obj
            if self.request.user.is_superuser:
                obj.save()
            else:
                member = get_bind_member(self.request.user)
                if member is None or obj.branch != member.branch:
                    messages.error(self.request, '%s失败，您不是%s的书记。' %
                                   ('添加' if self.org_obj is None else '修改', obj.branch))
                    if self.org_obj is None:
                        obj.delete()
                else:
                    obj.save()
