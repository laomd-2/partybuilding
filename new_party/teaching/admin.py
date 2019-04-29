import datetime
from collections import OrderedDict, Counter

from django.contrib import messages, admin
from common.base import *

from teaching.util import get_visual_activities, get_visual_credit
from info.util import get_visuable_members
from info.models import Member
from .models import Activity, TakePartIn, Sharing
from .resources import CreditResource, ActivityResource
from common.rules import *


@admin.register(Activity)
class ActivityAdmin(ImportExportAdmin):
    resource_class = ActivityResource
    list_display = ['name', 'date', 'end_time', 'atv_type', 'credit', 'get_branches']
    list_display_links = ['name']
    list_filter = ['date', 'end_time', 'atv_type', 'credit']
    search_fields = ['name']
    list_per_page = 15
    model_icon = 'fa fa-users'

    def get_exclude(self, request, obj=None):
        if not is_admin(request.user):
            return ['cascade', 'visualable_others']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            if not is_school_admin(request.user):
                member = self.bind_member(request)
                branches = [b.id for b in obj.branch.all()]
                if member is None or member['branch_id'] not in branches:
                    return [f.name for f in self.model._meta.fields]
            return []

    def save_model(self, request, obj, form, change):
        if not is_school_admin(request.user):
            member = self.bind_member(request)
            branches = map(int, request.POST['branch'].split(' '))
            if member is None or member['branch_id'] not in branches:
                if self.org_obj is None:
                    messages.warning(request, '您添加了其他党支部的活动。')
                else:
                    messages.error(request, '修改失败，权限不足。')
                    return
        obj.save()
        if obj.cascade:
            TakePartIn.objects.filter(activity_id=obj.id).update(credit=obj.credit)

    def get_queryset(self, request):
        return get_visual_activities(request.user)

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            m = self.bind_member(request)
            return m is not None and m['branch_id'] in [b.id for b in obj.branch.all()]
        return False

    def has_delete_permission(self, request, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            m = self.bind_member(request)
            return is_branch_manager(request.user) and m is not None and m['branch_id'] in obj.branch.all().all()
        return False

    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj):
            if is_school_admin(request.user) or obj is None or obj.visualable_others:
                return True
            m = self.bind_member(request)
            return m is not None and m['branch_id'] in [b.id for b in obj.branch.all()]
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


@admin.register(TakePartIn)
class CreditAdmin(ImportExportAdmin):
    resource_class = CreditResource
    list_display = ['member', 'activity', 'credit', 'last_modified']
    list_filter = ['activity__date', 'activity__atv_type', 'credit']
    search_fields = ['activity__name', 'member__name', 'member__netid']
    list_per_page = 15
    aggregate_fields = {"credit": "sum"}

    def get_queryset(self, request):
        qs = get_visual_credit(request.user)[1]
        if is_admin(request.user):
            return qs
        m = request.user.member
        if m is None:
            return qs.none()
        return qs.filter(member_id=m['netid'])

    def save_model(self, request, obj, form, change):
        if not is_school_admin(request.user):
            member = self.bind_member(request)
            branches = [b.id for b in obj.activity.branch.all()]
            if member is None or member['branch_id'] not in branches:
                messages.error(request, '%s失败，权限不足。' % ('添加' if self.org_obj is None else '修改'))
                return
        obj.save()

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['credit', 'last_modified']
        else:
            return []

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            tmp = ['member', 'activity', 'last_modified']
            if not is_school_admin(request.user):
                member = self.bind_member(request)
                branches = [b.id for b in obj.activity.branch.all()]
                if member is None or member['branch_id'] not in branches:
                    return tmp + ['credit']
            return tmp

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            m = self.bind_member(request)
            branches = [b.id for b in obj.activity.branch.all()]
            return m is not None and m['branch_id'] in branches
        return False

    def has_delete_permission(self, request, obj=None):
        if super(CreditAdmin, self).has_delete_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            m = self.bind_member(request)
            branches = [b.id for b in obj.activity.branch.all()]
            return m is not None and m['branch_id'] in branches
        return False

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "activity":
            kwargs["queryset"] = get_visual_activities(request.user)
        elif db_field.name == 'member':
            kwargs["queryset"] = get_visuable_members(Member, request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Sharing)
class SharingAdmin(AdminObject):
    list_display = ['member', 'title', 'when']
    search_fields = ['member__name', 'title']
    list_filter = ['when']
    list_per_page = 15

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        if is_admin(request.user):
            return ['member']
        return ['member', 'added']

    def get_queryset(self, request):
        qs = self.model.objects
        if not is_school_admin(request.user):  # 判断是否是党辅
            m = request.user.member
            if m is None:
                return qs.none()
            colleges = Member.objects.filter(branch_id=m['branch_id']).values('netid')
            return qs.filter(member_id__in=[m['netid'] for m in colleges])
        return qs.all().select_related('member')

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if is_admin(request.user) or obj is None:
                return True
            m = request.user.member
            return m is not None and m['netid'] == obj.member_id
        return False
