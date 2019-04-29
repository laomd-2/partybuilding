import os
from django.conf import settings
from django.contrib import admin, messages
from django.db.models import F

from info.resources import MemberResource
from common.rules import *
from common.base import AdminObject, ImportExportAdmin, get_chinese, get_old
from info.util import get_visuable_members, check_fields, get_visual_branch
from .models import School, Branch, Member, Dependency, Files, OldMember
from .actions import *


@admin.register(School)
class SchoolAdmin(AdminObject):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 15


@admin.register(Branch)
class BranchAdmin(AdminObject):
    actions = [merge_branch]
    list_display = ['branch_name', 'num_members', 'date_create']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_per_page = 15

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['school']

    def get_queryset(self, request):
        qs = self.model.objects.select_related('school')
        if request.user.is_superuser:
            return qs.all()
        if is_school_manager(request.user):  # 判断是否是党辅
            school = int(request.user.username[0])
            return School.objects.get(id=school).branch_set.all()
        else:
            member = self.bind_member(request)
            if member is None:
                return qs.none()
            return qs.filter(id=member['branch_id'])

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            if is_branch_manager(request.user):
                m = self.bind_member(request)
                return m is not None and m['branch_id'] == obj.id
        return False

    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            m = request.user.member
            return m is not None and m['branch_id'] == obj.id
        return False

    def has_delete_permission(self, request, obj=None):
        if super(BranchAdmin, self).has_delete_permission(request, obj):
            return obj is None or obj.id != 1
        return False


fields_, phases = Member.get_phases()


class MemberBaseAdmin(ImportExportAdmin):
    resource_class = MemberResource
    excel_template = os.path.join(settings.MEDIA_ROOT, 'Excel模板/成员信息.xlsx')

    list_display = fields_[:4] + ['gender', 'phone_number', 'major_in']
    fieldsets = [
        (k, {
            'fields': tuple(v),
            'classes': ('grp-collapse grp-closed',)
        }) for k, v in phases.items()
    ]

    ordering = ['second_branch_conference',
                'first_branch_conference',
                'key_develop_person_date',
                'activist_date',
                'branch', 'netid']

    def get_search_fields(self, request):
        if is_admin(request.user):
            return ['netid', 'name']
        return []

    def get_list_filter(self, request):
        if is_admin(request.user):
            general = ['second_branch_conference',
                       'first_branch_conference',
                       'key_develop_person_date',
                       'activist_date',
                       'first_talk_date',
                       'application_date']
            if is_branch_manager(request.user):
                return general
            else:
                return ['branch'] + general
        return []

    # def list_editable(self):
    #     if is_admin(request.user):
    #         res = []
    #         for k, v in phases.items():
    #             if k == '基本信息':
    #                 res += v[2:]
    #             else:
    #                 res += v
    #         res.remove('autobiography')
    #         res.remove('application_form')
    #         return res
    #     if is_member(request.user):  # 普通成员
    #         return phases['基本信息'][2:]
    #     return []

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        res = ['netid']
        if not is_school_admin(request.user):
            res.append('branch')
            if is_member(request.user):  # 普通成员
                m = request.user.member
                if m is None or m['netid'] != obj.netid:
                    return self.fields_
                for k, v in phases.items():
                    if k != '基本信息':
                        res += v
                res.remove('autobiography')
                res.remove('application_form')
        return res

    def get_queryset(self, request):
        queryset = get_visuable_members(self.model, request.user)
        orders = []
        for o in self.ordering:
            if o[0] == '-':
                orders.append(F(o[1:]).desc(nulls_last=True))
            else:
                orders.append(F(o).asc(nulls_last=True))
        return queryset.order_by(*orders)

    def save_model(self, request, obj, form, change):
        if change:
            if not is_school_admin(request.user):
                member = request.user.member
                if member is None or obj.branch_id != member['branch_id']:
                    old = get_old(obj)
                    messages.error(request, '%s失败，您没有此权限。' %
                                            '添加' if old is None else '修改')
                    return
            if check_fields(request, obj):
                obj.save()

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if obj is None or request.user.is_superuser:
                return True
            else:
                m = request.user.member
                if m is not None:
                    if is_branch_manager(request.user):
                        return m['branch_id'] == obj.branch_id
                    elif is_member(request.user):
                        return m['netid'] == obj.netid
                    elif is_school_manager(request.user):
                        return obj.branch.school_id == int(request.user.username[0])
        return False


@admin.register(Dependency)
class DependencyAdmin(AdminObject):
    list_display = ['from_1', 'to', 'days', 'scope']
    list_editable = ['days', 'scope']

    def get_list_display_links(self, request, list_display):
        if 'from_1' in list_display and is_school_admin(request.user):
            return ['from_1']
        else:
            return [None, ]


@admin.register(Files)
class FilesAdmin(AdminObject):
    list_display = ['name', 'get_notice', 'get_files']


@admin.register(Member)
class MemberAdmin(MemberBaseAdmin):
    actions = [add_activist, add_key_person, add_premember, add_fullmember]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'branch':
            kwargs["queryset"] = get_visual_branch(request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(OldMember)
class OldMemberAdmin(MemberBaseAdmin):
    pass
