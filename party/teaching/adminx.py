import datetime
from collections import OrderedDict, Counter

from django.contrib import messages
from django.contrib.auth import get_permission_codename

from common.base import AdminObject

from user.util import get_visuable_activities, get_bind_member, get_visuable_members
from info.models import Member
from .models import Activity, TakePartIn, Sharing
from .resources import CreditResource, ActivityResource
from common.rules import *
import xadmin


@xadmin.sites.register(Activity)
class ActivityAdmin(AdminObject):
    import_export_args = {
        'import_resource_class': ActivityResource,
        'export_resource_class': ActivityResource
    }

    # filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}

    list_display = ['name', 'date', 'end_time', 'atv_type', 'credit', 'get_branches']
    list_display_links = ['name']
    list_filter = ['date', 'end_time', 'atv_type', 'credit']
    search_fields = ['name']
    list_per_page = 15
    model_icon = 'fa fa-users'

    @property
    def exclude(self):
        if not is_admin(self.request.user):
            return ['cascade', 'visualable_others']
        return []

    def get_readonly_fields(self):
        obj = self.org_obj
        if obj is None:
            return []
        else:
            if not is_school_admin(self.request.user):
                member = self.bind_member
                branches = obj.branch.all().all().all()
                if member is None or member.branch not in branches:
                    return [f.name for f in self.model._meta.fields]
            return []

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = self.bind_member
            branches = map(int, self.request.POST['branch'].split(' '))
            if member is None or member['branch_id'] not in branches:
                if self.org_obj is None:
                    messages.warning(self.request, '您添加了其他党支部的活动。')
                else:
                    messages.error(self.request, '修改失败，权限不足。')
                    return
        obj.save()
        if obj.cascade:
            TakePartIn.objects.filter(activity_id=obj.id).update(credit=obj.credit)

    def queryset(self):
        return get_visuable_activities(self.request.user)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            return m is not None and m['branch_id'] in obj.branch.all().all()
        return False

    def has_delete_permission(self, request=None, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            m = self.bind_member
            return is_branch_manager(self.request.user) and m is not None and m['branch_id'] in obj.branch.all().all()
        return False

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if is_school_admin(self.request.user) or obj is None or obj.visualable_others:
                return True
            m = self.bind_member
            return m is not None and m['branch_id'] in obj.branch.all().all()
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
    import_export_args = {
        'import_resource_class': CreditResource,
        'export_resource_class': CreditResource
    }
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
        if not is_school_admin(self.request.user):  # 判断是否是党辅
            m = self.bind_member
            if m is None:
                return self.model.objects.none()
            if is_branch_manager(self.request.user):  # 支书
                colleges = [mm['netid'] for mm in Member.objects.filter(branch_id=m['branch_id']).values('netid')]
                return self.model.objects.filter(activity__date__gte=datetime.datetime(now.year, 1, 1),
                                                 member_id__in=colleges).select_related('member', 'activity')
            qs = self.model.objects.filter(member_id=m['netid'])
            if m.is_party_member():  # 党员查看全年
                return qs.select_related('member', 'activity')
            else:
                season = get_season(now)
                return qs.filter(activity__date__gte=season[0], activity__date__lt=season[1]) \
                    .select_related('member', 'activity')
        if self.request.user.is_superuser:
            return self.model.objects.all().select_related('member', 'activity')
        else:
            return self.model.objects.filter(member__branch__school_id=int(self.request.user.username[0]),
                                             member__first_branch_conference__isnull=False)

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = self.bind_member
            branches = obj.activity.branch.all()
            if member is None or member['branch_id'] not in branches:
                messages.error(self.request, '%s失败，权限不足。' % ('添加' if self.org_obj is None else '修改'))
                return
        obj.save()

    @property
    def data_charts(self):
        return None
        m = get_bind_member(self.request.user)
        if m is None and not is_school_manager(self.request.user):
            return None
        now = datetime.datetime.now()
        season = get_season(now)

        my_charts = {}
        if is_school_manager(self.request.user):
            school_id = int(self.request.user.username[0])
            members = Member.objects.filter(branch__school_id=school_id)
            all_take = self.model.objects.filter(member__branch__school_id=school_id,
                                                 activity__date__gte=datetime.datetime(now.year, 1, 1))  # 普通成员
        else:
            members = Member.objects.filter(branch=m.branch)
            all_take = self.model.objects.filter(member__branch=m.branch,
                                                 activity__date__gte=datetime.datetime(now.year, 1, 1))  # 普通成员
            if m.branch.id == 1:
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
                branches = [b.id for b in obj.activity.branch.all()]
                if member is None or member['branch_id'] not in branches:
                    return tmp + ['credit']
            return tmp

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            branches = [b.id for b in obj.activity.branch.all()]
            return m is not None and m['branch_id'] in branches
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
            branches = [b.id for b in obj.activity.branch.all()]
            return m is not None and m['branch_id'] in branches
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
        qs = self.model.objects
        if not is_school_admin(self.request.user):  # 判断是否是党辅
            m = self.bind_member
            if m is None:
                return qs.none()
            colleges = Member.objects.filter(branch_id=m['branch_id']).values('netid')
            return qs.filter(member_id__in=[m['netid'] for m in colleges])
        return qs.all().select_related('member')

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
            return m is not None and m['branch_id'] == obj.branch_id
        return False
