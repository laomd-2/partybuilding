from django.contrib import admin, messages
from django.contrib.auth import get_permission_codename
from import_export.admin import ImportExportModelAdmin
from info.resources import MemberResource
from user.models import get_bind_member
from .models import School, Branch, Member, Dependency
import xadmin


@xadmin.sites.register(School)
class SchoolAdmin(object):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))


@xadmin.sites.register(Branch)
class BranchAdmin(object):
    list_display = ['id', 'school', 'branch_name']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['school__name']
    model_icon = 'fa fa-user'
    list_per_page = 15

    def get_readonly_fields(self):
        if not self.request.user.has_perm('info.add_branch'):
            member = get_bind_member(self.request.user)
            if member is None or member.branch != obj:
                return ['school', 'branch_name', 'date_create']
            return ['school']
        return []

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

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))


@xadmin.sites.register(Member)
class MemberAdmin(object):
    resource_class = MemberResource

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

    fieldsets = [
        (k, {
            # 'classes': ('suit-tab', 'suit-tab-' + k,),
            'classes': ('grp-collapse grp-closed',),
            'fields': v
        }) for k, v in phases.items()
    ]

    # suit_form_tabs = [(k, k) for k in phases]

    def get_search_fields(self):
        if self.request.user.has_perm('info.add_member') or \
                self.request.user.has_perm('info.add_branch'):
            return ['netid', 'name']
        return []

    def get_list_filter(self):
        if self.request.user.has_perm('info.add_member') or \
                self.request.user.has_perm('info.add_branch'):
            return ['application_date',
                    'activist_date',
                    'key_develop_person_date',
                    'first_branch_conference',
                    'second_branch_conference']
        return []

    def get_readonly_fields(self):
        if not self.request.user.has_perm('info.add_member'):  # 普通成员
            res = ['branch', 'netid'] + self.phases['阶段1：入党考察'] + \
                  self.phases['阶段2：预备党员'] + self.phases['阶段3：正式党员']
            res.remove('youth_league_date')
            res.remove('constitution_group_date')
            return res
        return []

    def queryset(self):
        qs = self.model._default_manager.get_queryset()
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            member = get_bind_member(self.request.user)
            if member is None:
                return qs.none()
            else:
                if self.request.user.has_perm('info.add_member'):  # 支书
                    return qs.filter(branch=member.branch)
                else:
                    return qs.filter(netid=member.netid, branch=member.branch)  # 普通成员
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

    def save_model(self, obj, form, change):
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
                                       ('添加' if obj is None else '修改', obj.branch))
                    else:
                        obj.save()

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))


@xadmin.sites.register(Dependency)
class DependencyAdmin(object):
    list_display = ['from_1', 'to', 'days']
    list_editable = ['days']

    def get_list_display_links(self):
        if self.request.user.has_perm('info.add_branch'):
            return ['from_1']
        else:
            return [None, ]

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))
