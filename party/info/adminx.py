import os
from collections import OrderedDict
from django.conf import settings
from django.contrib import messages
from django.db.models import F, Q

from user.util import get_visuable_members
from info.resources import MemberResource
import xadmin
from xadmin.layout import Main, Fieldset
from common.rules import *
from common.base import AdminObject, get_old, get_chinese
from .models import School, Branch, Member, Dependency, Files
from .actions import *


@xadmin.sites.register(School)
class SchoolAdmin(AdminObject):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15


@xadmin.sites.register(Branch)
class BranchAdmin(AdminObject):
    actions = [MergeBranchAction]
    list_display = ['id', 'school', 'branch_name',
                    'num_members', 'date_create']
    list_display_links = ['branch_name']
    search_fields = ['branch_name', 'school__name']
    model_icon = 'fa fa-flag'
    list_per_page = 15

    def get_readonly_fields(self):
        if self.org_obj is None:
            return []
        return ['school']

    def queryset(self):
        qs = self.model.objects.select_related('school')
        if self.request.user.is_superuser:
            return qs.all()
        if is_school_manager(self.request.user):  # 判断是否是党辅
            school = int(self.request.user.username[0])
            return School.objects.get(id=school).branch_set.all()
        else:
            member = self.request.user.member
            if member is None:
                return qs.none()
            return qs.filter(id=member['branch_id'])

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            if is_branch_manager(self.request.user):
                m = self.request.user.member
                return m is not None and m['branch_id'] == obj.id
        return False


fields_, phases = Member.get_phases()


class MemberAdminMixin:
    @staticmethod
    def check_date_dep(obj, old):
        errors = []
        for dep in Dependency.objects.filter(Q(scope=2) | Q(scope=1 + int(not obj.is_sysu))):
            from_ = getattr(obj, dep.from_1)
            to = getattr(obj, dep.to)
            from_2 = None if old is None else getattr(old, dep.from_1)
            to2 = None if old is None else getattr(old, dep.to)
            if (from_ != from_2 or to != to2) and from_ and to:
                delta = to - from_
                if delta.days < dep.days:
                    errors.append((dep.from_1, dep.to, delta.days,
                                   dep.days_mapping[dep.days]))
        return errors

    @staticmethod
    def check_first_talk_date(obj, old):
        if obj.first_talk_date and obj.application_date:
            if old is None or (obj.application_date != old.application_date or
                               obj.first_talk_date != old.first_talk_date):
                days = (obj.first_talk_date - obj.application_date).days
                return days < 31
        return True

    @staticmethod
    def get_members(branch, names):
        res = []
        for name in names:
            try:
                res.append(Member.objects.filter(branch_id=branch, name=name).first())
            except Member.DoesNotExist:
                pass
        return res

    def check_fields(self, obj):
        old = get_old(obj)
        msg = messages.error

        errors = MemberAdminMixin.check_date_dep(obj, old)
        for e in errors:
            msg(self.request, "%s到%s需要%s，而%s只用了%d天。"
                % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
                   Member._meta.get_field(e[1]).verbose_name.strip('时间'),
                   e[3], obj, e[2]))
            return False
        # 检查首次组织谈话时间
        if obj.is_sysu and not self.check_first_talk_date(obj, old):
            msg(self.request, '未在一个月内完成首次组织谈话。')
            return False
        # 检查入党介绍人
        if obj.is_sysu and old is None or obj.recommenders != old.recommenders:
            for m in self.get_members(obj.branch_id, get_chinese(str(obj.recommenders))):
                if not m.is_real_party_member():
                    msg(self.request, '入党介绍人%s不是正式党员。' % m.name)
                    return False
        return True


@xadmin.sites.register(Member)
class MemberAdmin(AdminObject, MemberAdminMixin):
    actions = [ActivistAction, KeyPersonAction,
               PrememberAction, MemberAction]
    import_export_args = {'import_resource_class': MemberResource,
                          'export_resource_class': MemberResource}
    excel_template = os.path.join(settings.MEDIA_ROOT, 'Excel模板/成员信息.xlsx')
    list_display = fields_[1:4] + ['gender', 'phone_number', 'major_in']
    model_icon = 'fa fa-info'
    ordering = ['second_branch_conference',
                'first_branch_conference',
                'key_develop_person_date',
                'activist_date',
                'branch', 'netid']
    wizard_form_list = phases.items()

    form_layout = (
        Main(
            *[Fieldset(k, *v) for k, v in phases.items()]
        )
    )

    @property
    def data_charts(self):
        m = self.request.user.member
        if m is None and not is_school_admin(self.request.user):
            return None
        br = self.request.GET.get('_p_branch__id__exact')
        if is_school_manager(self.request.user):
            school_id = int(self.request.user.username[0])
            school = School.objects.get(id=school_id)
            if br is None:
                scope = school.name
                objects = self.model.objects.filter(branch_id__in=[branch.id for branch in school.branch_set.all()])
            else:
                try:
                    scope = Branch.objects.get(id=br).branch_name
                    objects = self.model.objects.filter(branch_id=br)
                except Branch.DoesNotExist:
                    return None
        elif self.request.user.is_superuser:
            if br is None:
                scope = ''
                objects = self.model.objects.all()
            else:
                try:
                    scope = Branch.objects.get(id=br).branch_name
                    objects = self.model.objects.filter(branch_id=br)
                except Branch.DoesNotExist:
                    return None
        else:
            scope = '党支部'
            objects = self.model.objects.filter(branch_id=m['branch_id'])
        if objects.count() == 0:
            return None
        my_charts = {
            'fenbu': {
                'title': scope + '成员分布',
            }
        }
        dates = OrderedDict([
            ('second_branch_conference', '正式党员'),
            ('first_branch_conference', '预备党员'),
            ('key_develop_person_date', '重点发展对象'),
            ('activist_date', '入党积极分子'),
            ('application_date', '入党申请人')
        ])

        fenbu = dict()
        for obj in objects:
            grade = obj.grade()
            fenbu.setdefault(grade, OrderedDict(
                [(k, 0) for k in dates.values()]))
            for d in dates:
                if getattr(obj, d):
                    fenbu[grade][dates[d]] += 1
                    break
        grades = list(sorted(fenbu.keys()))
        option = {
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'shadow'
                }
            },
            'toolbox': {
                'feature': {
                    'saveAsImage': {'show': True}
                }
            },
            'legend': {
                'data': list(dates.values())
            },
            'grid': {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': True
            },
            'xAxis': {
                'type': 'value'
            },
            'yAxis': {
                'type': 'category',
                'data': [g + '级' for g in grades]
            },
            'series': [
                {
                    'name': name,
                    'type': 'bar',
                    'stack': '总量',
                    'label': {
                        'normal': {
                            'show': False,
                            'position': 'insideRight'
                        }
                    },
                    'data': [fenbu[g][name] for g in grades]
                } for name in dates.values()
            ]
        }
        my_charts['fenbu']['option'] = option
        return my_charts

    @property
    def search_fields(self):
        if is_admin(self.request.user):
            return ['netid', 'name']
        return []

    @property
    def list_filter(self):
        if is_admin(self.request.user):
            general = ['second_branch_conference',
                       'first_branch_conference',
                       'key_develop_person_date',
                       'activist_date',
                       'first_talk_date',
                       'application_date']
            if is_branch_manager(self.request.user):
                return general
            else:
                return ['branch'] + general
        return []

    @property
    def list_editable(self):
        if is_admin(self.request.user):
            res = []
            for k, v in phases.items():
                if k == '基本信息':
                    res += v[2:]
                else:
                    res += v
            res.remove('autobiography')
            res.remove('application_form')
            return res
        if is_member(self.request.user):  # 普通成员
            return phases['基本信息'][2:]
        return []

    def get_readonly_fields(self):
        if self.org_obj is None:
            return []
        res = ['netid']
        if not is_school_admin(self.request.user):
            res.append('branch')
            if is_member(self.request.user):  # 普通成员
                m = self.request.user.member
                if m is None or m['netid'] != self.org_obj.netid:
                    return self.fields_
                for k, v in phases.items():
                    if k != '基本信息':
                        res += v
                res.remove('autobiography')
                res.remove('application_form')
        return res

    def queryset(self):
        queryset = get_visuable_members(self.request.user)
        orders = []
        for o in self.ordering:
            if o[0] == '-':
                orders.append(F(o[1:]).desc(nulls_last=True))
            else:
                orders.append(F(o).asc(nulls_last=True))
        return queryset.order_by(*orders)

    def save_models(self):
        if hasattr(self, 'new_obj'):
            if not is_school_admin(self.request.user):
                member = self.request.user.member
                if member is None or self.branch_id != member['branch_id']:
                    old = get_old(self)
                    messages.error(self.request, '%s失败，您没有此权限。' %
                                                 '添加' if old is None else '修改')
                    return
            if self.check_fields(self.new_obj):
                self.new_obj.save()

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if obj is None or self.request.user.is_superuser:
                return True
            else:
                m = self.request.user.member
                if m is not None:
                    if is_branch_admin(self.request.user):
                        return m['branch_id'] == obj.branch_id
                    elif is_member(self.request.user):
                        return m['netid'] == obj.netid
                elif is_school_manager(self.request.user):
                    return obj.branch.school_id == int(self.request.user.username[0])
        return False


@xadmin.sites.register(Dependency)
class DependencyAdmin(AdminObject):
    list_display = ['from_1', 'to', 'days', 'scope']
    list_editable = ['days', 'scope']
    model_icon = 'fa fa-angle-double-right'

    def get_list_display_links(self):
        if is_school_admin(self.request.user):
            return ['from_1']
        else:
            return [None, ]


@xadmin.sites.register(Files)
class FilesAdmin(AdminObject):
    list_display = ['name', 'get_notice', 'get_files']
    model_icon = "fa fa-files-o"
