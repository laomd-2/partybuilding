import datetime
from collections import OrderedDict, Counter

from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.db.models import Sum

from common.base import AdminObject

from common.user_util import get_visuable_activities, get_bind_member, get_visuable_members
from info.models import Member
from .models import Activity, TakePartIn, Sharing
from .resources import CreditResource, ActivityResource
from common.rules import *
import xadmin


@xadmin.sites.register(Activity)
class ActivityAdmin(AdminObject):
    # import_export_args = {'export_resource_class': ActivityResource}
    # filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}

    list_display = ['id', 'name', 'date', 'end_time', 'atv_type', 'credit', 'get_branches']
    list_display_links = ['name']
    list_filter = ['date', 'end_time', 'atv_type', 'credit']
    search_fields = ['name']
    list_per_page = 15
    model_icon = 'fa fa-users'

    def get_readonly_fields(self):
        obj = self.org_obj
        if obj is None:
            return []
        else:
            if not self.request.user.has_perm('info.add_branch'):
                member = self.bind_member
                branches = obj.branch.all()
                if member is None or member.branch not in branches:
                    return [f.name for f in self.model._meta.fields]
            return []

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = self.bind_member
            branches = map(int, self.request.POST['branch'].split(' '))
            if member is None or member.branch.id not in branches:
                if self.org_obj is None:
                    messages.warning(self.request, '您添加了其他党支部的活动。')
                else:
                    messages.error(self.request, '修改失败，您不是%s的书记。' %
                                   '或'.join([str(b) for b in obj.branch.all()]))
                    return
        obj.save()
        if obj.cascade:
            for o in TakePartIn.objects.filter(activity=obj):
                o.credit = obj.credit
                o.save()

    def queryset(self):
        return get_visuable_activities(self.request.user)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            return m is not None and m.branch in obj.branch.all()
        return False

    def has_delete_permission(self, request=None, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            m = self.bind_member
            return is_branch_manager(self.request.user) and m is not None and m.branch in obj.branch.all()
        return False

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if is_school_admin(self.request.user) or obj is None or obj.visualable_others:
                return True
            m = self.bind_member
            return m is not None and m.branch in obj.branch.all()
        return False


def get_season(now):
    seasons = [datetime.datetime(now.year, m, 1) for m in [3, 6, 9, 12]]
    seasons.append(datetime.datetime(now.year + 1, 3, 1))
    for i in range(1, len(seasons)):
        if now < seasons[i]:
            return seasons[i - 1], seasons[i]


def get_monthly_credit(all_take, month):
    months = OrderedDict((i + 1, {c: 0 for c in Activity.atv_type_choices}) for i in range(month))
    for t in all_take:
        d = t.activity.date
        if d.month in months:
            months[d.month][t.activity.atv_type] += t.credit
    option = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross',
                'crossStyle': {
                    'color': '#999'
                }
            }
        },
        'toolbox': {
            'feature': {
                'magicType': {'show': True, 'type': ['line', 'bar']},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'legend': {
            'data': Activity.atv_type_choices
        },
        'xAxis': [
            {
                'type': 'category',
                'data': ['%d月' % m for m in months.keys()],
                'axisPointer': {
                    'type': 'shadow'
                }
            }
        ],
        'yAxis': [
            {
                'type': 'value',
                'name': '学时数'
            },
        ],
        'series': [
            {
                'name': name,
                'type': 'bar',
                'data': [v[name] for v in months.values()]
            } for name in Activity.atv_type_choices
        ]
    }
    return option


def get_credit(all_take, members):
    credit_sum = Counter()
    for m in members:
        credit_sum[m] = 0
    for r in all_take:
        credit_sum[r.member] += r.credit
    credit_sum = list(credit_sum.items())
    credit_sum.sort(key=lambda x: x[1], reverse=True)
    option = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            }
        },
        'toolbox': {
            'feature': {
                'magicType': {'show': True, 'type': ['line', 'bar']},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        # 'grid': {
        #     'left': '3%',
        #     'right': '4%',
        #     'bottom': '3%',
        #     'containLabel': True
        # },
        'xAxis': {
            'type': 'category',
            'data': [x[0].name for x in credit_sum],
            'axisLabel': {
                'rotate': 45
            }
        },
        'yAxis': {
            'type': 'value'
        },
        'series': [{
            'data': [x[1] for x in credit_sum],
            'type': 'bar'
        }]
    }
    return option


@xadmin.sites.register(TakePartIn)
class CreditAdmin(AdminObject):
    import_export_args = {'import_resource_class': CreditResource}
    list_display = ['member', 'activity', 'credit', 'last_modified']
    list_filter = ['activity__date', 'activity__atv_type', 'credit']
    search_fields = ['activity__name', 'activity__date', 'member__name', 'member__netid']
    list_per_page = 15
    # style_fields = {'activity__name': 'fk-ajax'}

    model_icon = 'fa fa-bar-chart'
    aggregate_fields = {"credit": "sum"}

    @property
    def list_editable(self):
        if is_admin(self.request.user):
            return ['activity', 'credit']
        else:
            return []

    def queryset(self):
        now = datetime.datetime.now()
        qs = self.model._default_manager.get_queryset().filter(activity__date__gte=datetime.datetime(now.year, 1, 1))
        if not is_school_admin(self.request.user):  # 判断是否是党辅
            m = self.bind_member
            if m is None:
                return qs.none()
            if is_branch_manager(self.request.user):  # 支书
                colleges = Member.objects.filter(branch=m.branch)  # 找到该model 里该用户创建的数据
                return qs.filter(member__in=colleges)
            qs = qs.filter(member=m)
            if m.is_party_member():  # 党员查看全年
                return qs
            else:
                season = get_season(now)
                return qs.filter(activity__date__gte=season[0], activity__date__lt=season[1])
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(member__branch__school=int(self.request.user.username[0]),
                             member__first_branch_conference__isnull=False)

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = self.bind_member
            branches = obj.activity.branch.all()
            if member is None or member.branch not in branches:
                messages.error(self.request, '失败，请联系%s的支书来%s添加。' % ('或'.join(map(str, branches)),
                                                                    '添加' if self.org_obj is None else '修改'))
                return
        if self.org_obj is None:
            obj.credit = obj.activity.credit
        else:
            if obj.activity.cascade and obj.credit != obj.activity.credit:
                messages.error(self.request, '修改失败，该会议/活动的学时数是级联更新的。')
                return
        obj.save()

    @property
    def data_charts(self):
        m = get_bind_member(self.request.user)
        if m is None and not is_school_manager(self.request.user):
            return None
        now = datetime.datetime.now()
        season = get_season(now)

        my_charts = {}
        if is_school_manager(self.request.user):
            school_id = int(self.request.user.username[0])
            members = Member.objects.filter(branch__school=school_id)
            all_take = self.model.objects.filter(member__branch__school=school_id,
                                                 activity__date__gte=datetime.datetime(now.year, 1, 1))  # 普通成员
        else:
            members = Member.objects.filter(branch=m.branch)
            all_take = self.model.objects.filter(member__branch=m.branch,
                                                 activity__date__gte=datetime.datetime(now.year, 1, 1))  # 普通成员
            if m.branch == 1:
                my_charts['ranking'] = {
                    'title': '%d月-%d月考察学时排行榜' % (season[0].month, season[1].month),
                    'option': get_credit(all_take.filter(activity__date__gte=season[0],
                                                         activity__date__lt=season[1],
                                                         member__first_branch_conference=None),
                                         members.filter(first_branch_conference=None))
                }
                my_charts['ranking']['option']['color'] = ['#3398DB']
        my_charts['ranking2'] = {
            'title': '%d年度党员继续教育学时' % season[0].year,
            'option': get_credit(all_take.filter(member__first_branch_conference__isnull=False),
                                 members.filter(first_branch_conference__isnull=False))
        }
        if m is not None:
            my_charts['takepartin'] = {
                'title': '%d年各月份学时概览' % now.year,
                'option': get_monthly_credit(all_take.filter(member=m), now.month)
            }
        return my_charts

    @property
    def exclude(self):
        obj = self.org_obj
        if obj is None:
            return ['credit', 'last_modified']
        else:
            return []

    def get_readonly_fields(self):
        obj = self.org_obj
        if obj is None:
            return []
        else:
            tmp = ['member', 'activity', 'last_modified']
            if not is_school_admin(self.request.user):
                member = self.bind_member
                branches = obj.activity.branch.all()
                if member is None or member.branch not in branches:
                    return tmp + ['credit']
            return tmp

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            return m is not None and m.branch == obj.member.branch
        return False

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        if ('delete' not in self.remove_permissions) and \
                self.user.has_perm('%s.%s' % (self.app_label, codename)):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            m = self.bind_member
            return m is not None and m.branch == obj.member.branch
        return False

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "activity":
            kwargs["queryset"] = get_visuable_activities(self.request.user)
        elif db_field.name == 'member':
            kwargs["queryset"] = get_visuable_members(self.request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)


@xadmin.sites.register(Sharing)
class SharingAdmin(AdminObject):
    list_display = ['member', 'title', 'when']
    # list_editable = ['when']
    search_fields = ['member__name', 'title']
    list_filter = ['when']
    list_per_page = 15
    model_icon = 'fa fa-book'

    def get_readonly_fields(self):
        if self.request.user.is_superuser:
            return []
        if is_admin(self.request.user):
            return ['member']
        return ['member', 'added']

    # style_fields = {'activity__name': 'fk-ajax'}

    # model_icon = 'fa fa-bar-chart'

    def queryset(self):
        qs = self.model._default_manager.get_queryset()
        if not is_school_admin(self.request.user):  # 判断是否是党辅
            m = self.bind_member
            if m is None:
                return qs.none()
            colleges = Member.objects.filter(branch=m.branch)  # 找到该model 里该用户创建的数据
            return qs.filter(member__in=colleges)
        return qs

    def formfield_for_dbfield(self, db_field, **kwargs):
        if not self.request.user.is_superuser:
            if db_field.name == 'member':
                if is_school_admin(self.request.user):
                    kwargs["queryset"] = Member.objects.all()
                else:
                    m = self.bind_member
                    if m is None:
                        kwargs["queryset"] = Member.objects.none()
                    else:
                        kwargs["queryset"] = Member.objects.filter(branch=m.branch)
        return super().formfield_for_dbfield(db_field, **kwargs)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            return m is not None and m == obj.member
        return False
