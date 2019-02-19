from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from common.base import AdminObject
from django.db.models import Q
from info.models import Member
from user.models import get_bind_member
from .models import Activity, TakePartIn
from .resources import CreditResource
from common.rules import *
import xadmin


@xadmin.sites.register(Activity)
class ActivityAdmin(AdminObject):
    # import_export_args = {'import_resource_class': ActivityResource}
    # filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}

    list_display = ['name', 'date', 'end_time', 'credit', 'get_branches']

    # def get_list_display(self):
    #     res = self.base_list_display
    #     if self.request.user.has_perm('info.add_member') or self.request.user.has_perm('info.add_branch'):
    #         return ['id'] + res
    #     return res

    list_filter = ['date', 'end_time', 'credit']
    search_fields = ['name']
    list_per_page = 15
    model_icon = 'fa fa-users'

    def get_readonly_fields(self):
        obj = self.org_obj
        if obj is None:
            return []
        else:
            if not self.request.user.has_perm('info.add_branch'):
                member = get_bind_member(self.request.user)
                branches = obj.branch.all()
                if member is None or member.branch not in branches:
                    return ['name', 'date', 'end_time', 'credit', 'visualable_others', 'branch']
            return []

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = get_bind_member(self.request.user)
            branches = map(int, self.request.POST['branch'].split(' '))
            if member is None or member.branch.id not in branches:
                if self.org_obj is None:
                    messages.warning(self.request, '您添加了其他党支部的活动。')
                else:
                    messages.error(self.request, '修改失败，您不是%s的书记。' %
                                   '或'.join([str(b) for b in obj.branch.all()]))
                    return
        obj.save()

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            try:
                m = Member.objects.get(netid=self.request.user)
                return self.model.objects.filter(Q(branch__id__contains=m.branch.id) |
                                                 Q(visualable_others=True)).distinct()
            except ObjectDoesNotExist:
                return self.model.objects.none()
        return self.model.objects.all().distinct()

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
            return m is not None and m.branch in obj.branch.all()
        return False

    def has_view_permission(self, obj=None):
        if super().has_view_permission(obj):
            if is_school_admin(self.request.user) or obj is None or obj.visualable_others:
                return True
            m = self.bind_member
            return m is not None and m.branch in obj.branch.all()
        return False


@xadmin.sites.register(TakePartIn)
class CreditAdmin(AdminObject):
    resource_class = CreditResource
    search_fields = ['activity__name', 'activity__date', 'member__name']

    list_display = ['member', 'activity', 'credit']
    list_filter = ['activity__date', 'credit']
    list_per_page = 15

    model_icon = 'fa fa-bar-chart'
    aggregate_fields = {"credit": "sum"}

    # data_charts = {
    #     "user_count": {'title': "学时统计", "x-field": "date", "y-field": "credit",
    #                    "order": ('date',)
    #                    }
    # }

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            m = get_bind_member(self.request.user)
            if m is None:
                return self.model.objects.none()
            if self.request.user.has_perm('info.add_member'):  # 支书
                colleges = Member.objects.filter(branch=m.branch)  # 找到该model 里该用户创建的数据
                return self.model.objects.filter(member__in=colleges)
            return self.model.objects.filter(member=m)  # 普通成员
        return self.model.objects.all()

    def save_models(self):
        obj = self.new_obj
        if not is_school_admin(self.request.user):
            member = get_bind_member(self.request.user)
            branches = obj.activity.branch.all()
            if member is None or member.branch not in branches:
                if self.org_obj is None:
                    messages.error(self.request, '失败，请联系%s的支书来添加。' % ('或'.join(map(str, branches))))
                    return
                else:
                    obj.credit = obj.activity.credit
        if self.org_obj is None:
            obj.credit = obj.activity.credit
        obj.save()

    @property
    def exclude(self):
        obj = self.org_obj
        if obj is None:
            return ['credit']
        else:
            return []

    def get_readonly_fields(self):
        obj = self.org_obj
        if obj is None:
            return []
        else:
            if not self.request.user.has_perm('info.add_branch'):
                member = get_bind_member(self.request.user)
                branches = obj.activity.branch.all()
                if member is None or member.branch not in branches:
                    return ['member', 'activity', 'credit']
            return ['member', 'activity']

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if is_school_admin(self.request.user) or obj is None:
                return True
            m = self.bind_member
            return m is not None and m.branch == obj.member.branch
        return False

    def has_delete_permission(self, request=None, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            m = self.bind_member
            return m is not None and m.branch == obj.member.branch
        return False
