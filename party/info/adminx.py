from collections import OrderedDict
from django.contrib import messages

from common.user_util import get_visuable_members, get_bind_member
from info.resources import MemberResource
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
    search_fields = ['branch_name', 'school__name']
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


@xadmin.sites.register(Member)
class MemberAdmin(AdminObject):
    import_export_args = {'import_resource_class': MemberResource,
                          'export_resource_class': MemberResource}

    fields_ = [field.name for field in Member._meta.fields]
    list_display = fields_[1:4] + ['gender', 'phone_number', 'major_in']

    model_icon = 'fa fa-info'
    list_per_page = 15
    # list_editable = list_display[1:]
    # relfield_style = 'fk_ajax'

    fenge = OrderedDict([
        ('application_date', '基本信息'),
        ('league_promotion_date_a', '一、申请入党'),
        ('democratic_appraisal_date', '二、入党积极分子的确定和培养'),
        ('autobiography_date', '三、发展对象的确定和考察'),
        ('oach_date', '四、预备党员的吸收'),
        ('', '五、预备党员的教育考察和转正')])
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
        if m is None:
            return None
        my_charts = {
            'fenbu': {
                'title': '党支部成员分布',
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
        for obj in self.model.objects.all():
            grade = str(obj.netid)[:2]
            fenbu.setdefault(grade, OrderedDict([(k, 0) for k in dates.values()]))
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
        return res

    def queryset(self):
        return get_visuable_members(self.request.user)

    @staticmethod
    def check_dep(obj):
        errors = []
        for dep in Dependency.objects.all():
            from_ = getattr(obj, dep.from_1)
            to = getattr(obj, dep.to)
            if from_ and to:
                delta = to - from_
                if delta.days < dep.days:
                    errors.append((dep.from_1, dep.to, delta.days, dep.days_mapping[dep.days]))
        return errors

    def save_models(self):
        if hasattr(self, 'new_obj'):
            obj = self.new_obj
            errors = self.check_dep(obj)
            msg = messages.error if self.org_obj is None else messages.warning
            for e in errors:
                msg(self.request, "%s到%s需要%s，而%s只用了%d天。"
                    % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
                       Member._meta.get_field(e[1]).verbose_name.strip('时间'),
                       e[3], obj, e[2]))
                if self.org_obj is None:
                    return
            if self.request.user.is_superuser:
                obj.save()
            else:
                member = self.bind_member
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
