import re
from collections import OrderedDict
from user.util import get_visuable_members, get_bind_member
from info.resources import MemberResource
import xadmin
from xadmin.layout import Main, Fieldset
from common.rules import *
from common.base import AdminObject
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
        qs = self.model._default_manager.get_queryset()
        if self.request.user.is_superuser:
            return qs
        if self.request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            school = int(self.request.user.username[0])
            return qs.filter(school__id=school)
        else:
            member = self.bind_member
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


def get_chinese(s):
    pattern = "[\u4e00-\u9fa5]+"
    regex = re.compile(pattern)
    return regex.findall(s)


@xadmin.sites.register(Member)
class MemberAdmin(AdminObject):
    actions = [ActivistAction, KeyPersonAction,
               PrememberAction, MemberAction, ActivityAction]
    import_export_args = {'import_resource_class': MemberResource,
                          'export_resource_class': MemberResource}

    fields_ = [field.name for field in Member._meta.fields]
    list_display = fields_[1:4] + ['gender', 'phone_number', 'major_in']

    model_icon = 'fa fa-info'
    list_per_page = 15
    # list_editable = list_display[1:]
    ordering = ['second_branch_conference',
                'first_branch_conference',
                'key_develop_person_date',
                'activist_date',
                'branch', 'netid']

    fenge = OrderedDict([
        ('application_date', '基本信息'),
        ('activist_date', '申请入党'),
        ('democratic_appraisal_date', '入党积极分子的确定和培养'),
        ('recommenders_date', '发展对象的确定和考察'),
        ('oach_date', '预备党员的吸收'),
        ('', '预备党员的教育考察和转正')])
    phases = dict()
    last = 0
    for k, v in fenge.items():
        if k:
            tmp = fields_.index(k)
        else:
            tmp = -1
        phases[v] = fields_[last: tmp]
        last = tmp
    wizard_form_list = phases.items()

    form_layout = (
        Main(
            *[Fieldset(k, *v) for k, v in phases.items()]
        )
    )

    @property
    def data_charts(self):
        m = get_bind_member(self.request.user)
        if m is None and not is_school_admin(self.request.user):
            return None
        if is_school_manager(self.request.user):
            school_id = int(self.request.user.username[0])
            scope = School.objects.get(id=school_id).name
            objects = self.model.objects.filter(branch__school=school_id)
        elif self.request.user.is_superuser:
            scope = ''
            objects = self.model.objects.all()
        else:
            scope = '党支部'
            objects = self.model.objects.filter(branch=m.branch)
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
            grade = str(obj.netid)[:2]
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

    def get_readonly_fields(self):
        if self.org_obj is None:
            return []
        res = ['branch', 'netid']
        if is_member(self.request.user):  # 普通成员
            m = self.bind_member
            if m is None or m.netid != self.org_obj.netid:
                return self.fields_
            for k, v in self.phases.items():
                if k != '基本信息':
                    res += v
            res.remove('autobiography')
            res.remove('application_form')
        return res

    def queryset(self):
        return get_visuable_members(self.request.user)

    @staticmethod
    def check_date_dep(obj: Member, old):
        errors = []
        for dep in Dependency.objects.all():
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
    def check_first_talk_date(obj, old: Member):
        if obj.first_talk_date and obj.application_date:
            if old is None or (obj.application_date != old.application_date or
                               obj.first_talk_date != old.first_talk_date):
                days = (obj.first_talk_date - obj.application_date).days
                return days < 31
        return True

    @staticmethod
    def get_members(names):
        res = []
        for name in names:
            try:
                res.append(Member.objects.get(name=name))
            except:
                pass
        return res

    def get_old(self):
        try:
            return Member.objects.get(netid=self.new_obj.netid)
        except Member.DoesNotExist:
            return None

    def save_models(self):
        if hasattr(self, 'new_obj'):
            obj = self.new_obj
            old = self.get_old()
            msg = messages.error

            errors = self.check_date_dep(obj, old)
            for e in errors:
                msg(self.request, "%s到%s需要%s，而%s只用了%d天。"
                    % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
                       Member._meta.get_field(e[1]).verbose_name.strip('时间'),
                       e[3], obj, e[2]))
            else:
                if not self.check_first_talk_date(obj, old):
                    msg(self.request, '未在一个月内完成首次组织谈话。')
                    return
                persons = self.get_members(get_chinese(str(obj.contacts)))
                if persons:
                    for m in persons:
                        if m.is_real_party_member():
                            break
                    else:
                        if old is None or obj.contacts != old.contacts:
                            msg(self.request, '培养联系人至少需要一名正式党员。')
                            return
                        else:
                            messages.warning(self.request, '培养联系人至少需要一名正式党员。')
                for m in self.get_members(get_chinese(str(obj.recommenders))):
                    if not m.is_real_party_member():
                        if old is None or obj.recommenders != old.recommenders:
                            msg(self.request, '入党介绍人%s不是正式党员。' % m.name)
                            return
                        else:
                            messages.warning(self.request, '入党介绍人%s不是正式党员。' % m.name)
                if self.request.user.is_superuser:
                    obj.save()
                else:
                    member = self.bind_member
                    if member is None or obj.branch != member.branch:
                        messages.error(self.request, '%s失败，您不是%s的书记。' %
                                       ('添加' if old is None else '修改', obj.branch))
                        if old is None:
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
    model_icon = 'fa fa-angle-double-right'

    def get_list_display_links(self):
        if self.request.user.has_perm('info.add_branch'):
            return ['from_1']
        else:
            return [None, ]


@xadmin.sites.register(Files)
class FilesAdmin(AdminObject):
    list_display = ['name', 'get_notice', 'get_files']
    model_icon = "fa fa-files-o"
