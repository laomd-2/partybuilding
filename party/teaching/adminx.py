from django.contrib import messages
from django.contrib.auth import get_permission_codename

from common.base import AdminObject
from common.utils import Cache
from info.util import get_visuable_members
from .util import *
from .models import *
from .resources import CreditResource, ActivityResource
from common.rules import *
import xadmin

cache_dict = dict()


def branch_in(branch, activity, branches):
    cache = cache_dict.get((branch, activity))
    if cache is None:
        cache = cache_dict[(branch, activity)] = Cache(5)
    res = cache.get()
    if res is None:
        res = branches.all().filter(branch_name=Branch.objects.get(id=branch).branch_name).exists()
        cache.set(res)
    return res


@xadmin.sites.register(Activity)
class ActivityAdmin(AdminObject):
    import_export_args = {
        'import_resource_class': ActivityResource,
        'export_resource_class': ActivityResource
    }

    # filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}

    list_display = ['id', 'name', 'date', 'atv_type', 'credit', 'get_branches']
    list_exclude = ['image%d' % (i + 1) for i in range(5)]
    list_display_links = ['name']
    list_filter = ['date', 'atv_type', 'credit']
    search_fields = ['name']
    button_pull_left = True
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
                member = self.request.user.member
                if member is None or not branch_in(member['branch_id'], obj.id, obj.branch):
                    return [f.name for f in self.model._meta.fields]
            return []

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = self.request.user.member
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
        return get_visual_activities(self.request.user)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.request.user.member
            return m is not None and branch_in(m['branch_id'], obj.id, obj.branch)
        return False

    def has_delete_permission(self, request=None, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            if is_branch_manager(self.request.user):
                m = self.request.user.member
                return m is not None and branch_in(m['branch_id'], obj.id, obj.branch)
        return False

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if is_school_admin(self.request.user) or obj is None or obj.visualable_others:
                return True
            m = self.request.user.member
            return m is not None and branch_in(m['branch_id'], obj.id, obj.branch)
        return False


class CreditAdminBase(AdminObject):
    import_export_args = {
        'import_resource_class': CreditResource,
        'export_resource_class': CreditResource
    }
    list_display = ['get_member_netid', 'get_member_name', 'activity', 'get_activity_type', 'get_activity_date',
                    'credit']
    list_exclude = ['id', 'member']
    list_display_links = ['get_member_netid']

    @property
    def list_filter(self):
        base = []
        if is_school_admin(self.request.user):
            base.append('member__branch')
        return base + ['activity__date', 'activity__atv_type', 'credit']

    search_fields = ['activity__name', 'member__name', 'member__netid']
    list_per_page = 15
    # style_fields = {'activity__name': 'fk-ajax'}

    model_icon = 'fa fa-bar-chart'

    @property
    def aggregate_fields(self):
        if is_member(self.request.user):
            return {"credit": "sum"}
        return None

    @property
    def list_editable(self):
        if is_admin(self.request.user):
            return ['activity', 'credit']
        else:
            return []

    def queryset(self):
        qs = get_visual_credit(self.request.user, self.model)[1]
        if is_admin(self.request.user):
            return qs
        m = self.request.user.member
        if m is None:
            return qs.none()
        return qs.filter(member_id=m['netid'])

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = self.request.user.member
            if member is None or not branch_in(member['branch_id'], obj.activity_id, obj.activity.branch):
                messages.error(self.request, '%s失败，权限不足。' % ('添加' if self.org_obj is None else '修改'))
                return
        obj.save()

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
                member = self.request.user.member
                if member is None or not branch_in(member['branch_id'], obj.activity_id, obj.activity.branch):
                    return tmp + ['credit']
            return tmp

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.request.user.member
            return m is not None and branch_in(m['branch_id'], obj.activity_id, obj.activity.branch)
        return False

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        if ('delete' not in self.remove_permissions) and \
                self.user.has_perm('%s.%s' % (self.app_label, codename)):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            m = self.request.user.member
            return m is not None and branch_in(m['branch_id'], obj.activity_id, obj.activity.branch)
        return False

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "activity":
            kwargs["queryset"] = get_visual_activities(self.request.user)
        return super().formfield_for_dbfield(db_field, **kwargs)


@xadmin.sites.register(TakePartIn)
class CreditAdmin(CreditAdminBase):
    @property
    def list_charts(self):
        return get_list_chart(self.request, TakePartIn)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'member':
            kwargs["queryset"] = get_visuable_members(Member, self.request.user). \
                filter(first_branch_conference__isnull=False)
        return super().formfield_for_dbfield(db_field, **kwargs)


@xadmin.sites.register(TakePartIn2)
class CreditAdmin2(CreditAdminBase):
    @property
    def list_charts(self):
        m = self.request.user.member
        if m is None or m['branch_id'] != 85:
            return None
        my_charts = {}
        year, all_take = get_visual_credit(self.request.user, self.model)

        season = get_season(datetime.datetime.today())
        kaocha = all_take.filter(activity__date__gte=season[0],
                                 activity__date__lt=season[1])
        members = Member.objects.filter(branch_id=m['branch_id'], first_branch_conference__isnull=True)
        if kaocha.count():
            my_charts['kaocha'] = {
                'title': '%d月-%d月考察学时排行榜' % (season[0].month, season[1].month),
                'option': get_credit(kaocha, members)
            }
            my_charts['kaocha']['option']['color'] = ['#3398DB']
        return my_charts

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'member':
            kwargs["queryset"] = get_visuable_members(Member, self.request.user). \
                filter(first_branch_conference__isnull=True)
        return super().formfield_for_dbfield(db_field, **kwargs)


@xadmin.sites.register(Sharing)
class SharingAdmin(AdminObject):
    list_display = ['member', 'title', 'when']
    list_display_links = ['title']
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
            m = self.request.user.member
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
                    m = self.request.user.member
                    if m is None:
                        kwargs["queryset"] = Member.objects.none()
                    else:
                        kwargs["queryset"] = Member.objects.filter(branch=m.branch)
        return super().formfield_for_dbfield(db_field, **kwargs)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if self.request.user.is_superuser or obj is None:
                return True
            m = self.request.user.member
            if m is not None:
                if is_branch_manager(self.request.user):
                    return m['branch_id'] == obj.member.branch_id
                else:
                    return m['netid'] == obj.member_id
        return False

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if self.request.user.is_superuser:
                return True
            m = self.request.user.member
            return m is not None and m['branch_id'] == 85
        return False
