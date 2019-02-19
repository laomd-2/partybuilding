from django.contrib import messages
from info.resources import MemberResource
from user.models import get_bind_member
from xadmin.layout import Main, Fieldset
from .models import School, Branch, Member, Dependency
import xadmin
from common.rules import *
from common.base import AdminObject


@xadmin.sites.register(School)
class SchoolAdmin(AdminObject):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15


@xadmin.sites.register(Branch)
class BranchAdmin(AdminObject):
    list_display = ['id', 'school', 'branch_name', 'date_create']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['school__name']
    model_icon = 'fa fa-user'
    list_per_page = 15

    def get_readonly_fields(self):
        if self.org_obj is None:
            return []
        return ['school']

    def queryset(self):
        qs = self.model._default_manager.get_queryset()
        if self.request.user.is_superuser:
            return qs
        if self.request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            school = int(self.request.user.username[0])
            return qs.filter(school__id=school)
        else:
            member = get_bind_member(self.request.user)
            if member is None:
                return qs.none()
            else:
                return qs.filter(school=member.branch.school)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            return m is not None and m.branch == obj
        return False


@xadmin.sites.register(Member)
class MemberAdmin(AdminObject):
    guarded_model = True
    import_export_args = {'import_resource_class': MemberResource}

    fields_ = [field.name for field in Member._meta.fields]
    list_display = fields_[1:5] + ['phone_number', 'major_in']

    model_icon = 'fa fa-info'
    list_per_page = 15
    # list_editable = list_display[1:]
    # relfield_style = 'fk_ajax'

    phases = dict()
    phases['基本信息'] = fields_[:10]
    phases['阶段1：入党考察'] = fields_[10:19]
    phases['阶段2：预备党员'] = fields_[19:28]
    phases['阶段3：正式党员'] = fields_[28:]

    wizard_form_list = phases.items()

    form_layout = (
        Main(
            *[Fieldset(k, *v) for k, v in wizard_form_list]
        )
    )

    def get_search_fields(self):
        if is_admin(self.request.user):
            return ['netid', 'name']
        return []

    def get_list_filter(self):
        if is_admin(self.request.user):
            return ['application_date',
                    'activist_date',
                    'key_develop_person_date',
                    'first_branch_conference',
                    'second_branch_conference']
        return []

    def get_readonly_fields(self):
        if is_member(self.request.user):  # 普通成员
            m = self.bind_member
            if m is None or m.netid != self.org_obj.netid:
                return self.fields_
            res = ['branch', 'netid'] + self.phases['阶段1：入党考察'] + \
                  self.phases['阶段2：预备党员'] + self.phases['阶段3：正式党员']
            res.remove('youth_league_date')
            res.remove('constitution_group_date')
            return res
        return []

    def queryset(self):
        qs = self.model._default_manager.get_queryset()
        if not is_school_admin(self.request.user):  # 判断是否是党辅
            member = get_bind_member(self.request.user)
            if member is None:
                return qs.none()
            else:
                if is_branch_manager(self.request.user):  # 支书
                    return qs.filter(branch=member.branch)
                elif is_member(self.request.user):
                    return qs.filter(netid=member.netid, branch=member.branch)  # 普通成员
                else:
                    return qs.none()
        return qs

    @staticmethod
    def check_dep(obj):
        errors = []
        for dep in Dependency.objects.all():
            from_ = getattr(obj, dep.from_1)
            to = getattr(obj, dep.to)
            if from_ and to:
                delta = to - from_
                if delta.days < dep.days:
                    errors.append((dep.from_1, dep.to, delta.days, dep.days))
        return errors

    def save_models(self):
        if hasattr(self, 'new_obj'):
            obj = self.new_obj
            if obj is not None:
                errors = self.check_dep(obj)
                for e in errors:
                    messages.error(self.request,
                                   "%s到%s需要%d天，而%s只用了%d天。"
                                   % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
                                      Member._meta.get_field(e[1]).verbose_name.strip('时间'),
                                      e[3], obj, e[2]))
                    break
                else:
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

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if obj is None or self.request.user.is_superuser:
                return True
            else:
                m = self.bind_member
                if m is not None:
                    if is_branch_admin(self.request.user):
                        return m.branch == obj.branch
                    elif is_member(self.request.user):
                        return m.netid == obj.netid
        return False

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if obj is None or is_school_admin(self.request.user):
                return True
            else:
                m = self.bind_member
                if m is not None:
                    if is_branch_manager(self.request.user):
                        return m.branch == obj.branch
                    elif is_member(self.request.user):
                        return m.netid == obj.netid
        return False


@xadmin.sites.register(Dependency)
class DependencyAdmin(AdminObject):
    list_display = ['from_1', 'to', 'days']
    list_editable = ['days']

    def get_list_display_links(self):
        if self.request.user.has_perm('info.add_branch'):
            return ['from_1']
        else:
            return [None, ]
