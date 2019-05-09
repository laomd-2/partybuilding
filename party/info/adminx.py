from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.db.models import F
from .util import get_visuable_members, get_visual_branch, check_fields
from info.resources import MemberResource
import xadmin
from xadmin.layout import Main, Fieldset, Side
from common.rules import *
from common.base import AdminObject, get_old
from .models import *
from .actions import *
from common.utils import Cache


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
    list_display = ['branch_name', 'get_leaders', 'num_members', 'date_create']
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

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.request.user.member
            return m is not None and m['branch_id'] == obj.id
        return False

    def has_delete_permission(self, request=None, obj=None):
        if obj is None:
            obj = request
        codename = get_permission_codename('delete', Branch._meta)
        has = self.user.has_perm('%s.%s' % (Branch._meta.app_label, codename))
        return has and (obj is None or obj.id != 1)


fields_, phases = Member.get_phases()


class MemberBaseAdmin(AdminObject):
    actions = [ActivistAction, KeyPersonAction,
               PrememberAction, MemberAction]
    import_export_args = {'import_resource_class': MemberResource,
                          'export_resource_class': MemberResource}

    list_display = fields_[:4] + ['gender', 'phone_number', 'major_in', 'years']
    list_display_links = ('netid',)
    model_icon = 'fa fa-info'
    ordering = ['branch', 'netid', 'second_branch_conference',
                'first_branch_conference',
                'key_develop_person_date',
                'activist_date']
    wizard_form_list = phases.items()

    form_layout = (
        Main(
            *[Fieldset(k, *v) for k, v in phases.items()]
        ),
        Side(
            Fieldset('关系转出', 'out_date', 'out_place'),
            Fieldset('其他信息', 'remarks')
        )
    )

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
                    return fields_
                for k, v in phases.items():
                    if k != '基本信息':
                        res += v
                res.extend(['out_date', 'out_place', 'remarks'])
        return res

    def queryset(self):
        queryset = get_visuable_members(self.model, self.request.user)
        orders = []
        for o in self.ordering:
            if o[0] == '-':
                orders.append(F(o[1:]).desc(nulls_last=True))
            else:
                orders.append(F(o).asc(nulls_last=True))
        return queryset.order_by(*orders)

    def save_models(self):
        if hasattr(self, 'new_obj'):
            obj = self.new_obj
            if not is_school_admin(self.request.user):
                member = self.request.user.member
                if member is None or obj.branch_id != member['branch_id']:
                    old = get_old(obj)
                    messages.error(self.request, '%s失败，您没有此权限。' %
                                                 '添加' if old is None else '修改')
                    return
            if check_fields(self.request, obj):
                obj.save()

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


@xadmin.sites.register(Member)
class MemberAdmin(MemberBaseAdmin):
    list_display = fields_[:4] + ['gender', 'phone_number', 'major_in', 'years']
    my_export = True
    show_chart = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'branch':
            kwargs["queryset"] = get_visual_branch(self.request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)

    @property
    def data_charts(self):
        username = self.request.user.username
        cache = charts.get(username)
        if cache is None:
            cache = charts[username] = Cache(3)
            res = get_chart(self.request)
            cache.set(res)
        else:
            res = cache.get()
            if res is None:
                res = get_chart(self.request)
                cache.set(res)
        return res


charts = dict()


def get_chart(request):
    m = request.user.member
    if m is None and not is_school_admin(request.user):
        return None
    br = request.GET.get('_p_branch__id__exact') or request.GET.get('_rel_branch__id__exact')

    important_dates = ('netid', 'application_date', 'activist_date',
                       'key_develop_person_date', 'first_branch_conference',
                       'second_branch_conference')
    if is_school_manager(request.user):
        if br is None:
            school = request.user.school
            scope = school['name']
            objects = Member.objects.filter(branch__school_id=school['id']).values(*important_dates)
        else:
            try:
                scope = Branch.objects.get(id=br).branch_name
                objects = Member.objects.filter(branch_id=br).values(*important_dates)
            except Branch.DoesNotExist:
                return None
    elif request.user.is_superuser:
        if br is None:
            scope = '全部'
            objects = Member.objects.all().values(*important_dates)
        else:
            try:
                scope = Branch.objects.get(id=br).branch_name
                objects = Member.objects.filter(branch_id=br).values(*important_dates)
            except Branch.DoesNotExist:
                return None
    else:
        scope = '党支部'
        objects = Member.objects.filter(branch_id=m['branch_id']).values(*important_dates)
    if not objects.exists():
        return None
    my_charts = {
        'fenbu': {
            'title': scope + '成员分布'
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
        grade = '20' + str(obj['netid'])[:2]
        fenbu.setdefault(grade, OrderedDict(
            [(k, 0) for k in dates.values()]))
        for d in dates:
            if obj[d]:
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


@xadmin.sites.register(OldMember)
class OldMemberAdmin(MemberBaseAdmin):
    pass
