from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from import_export.admin import ImportExportModelAdmin
from django.db.models import Q
from info.models import Member
from user.models import get_bind_member
from .models import Activity, TakePartIn
from .resources import CreditResource


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    # import_export_args = {'import_resource_class': ActivityResource}
    # filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}

    base_list_display = ['name', 'date', 'end_time', 'credit', 'get_branches']

    def get_list_display(self, request):
        res = self.base_list_display
        if request.user.has_perm('info.add_member') or request.user.has_perm('info.add_branch'):
            return ['id'] + res
        return res

    list_filter = ['date', 'end_time', 'credit']
    search_fields = ['name']
    list_per_page = 15
    model_icon = 'fa fa-users'

    def get_readonly_fields(self, request, obj=None):
        if self.org_obj is None:
            return []
        else:
            if not request.user.has_perm('info.add_branch'):
                member = get_bind_member(request.user)
                branches = self.org_obj.branch.all()
                if member is None or member.branch not in branches:
                    return ['name', 'date', 'end_time', 'credit', 'visualable_others', 'branch']
            return []

    def get_queryset(self, request):
        if not request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            try:
                m = Member.objects.get(netid=request.user)
                return self.model.objects.filter(Q(branch__id__contains=m.branch.id) |
                                                 Q(visualable_others=True)).distinct()
            except ObjectDoesNotExist:
                return self.model.objects.none()
        return self.model.objects.all().distinct()

    def save_model(self, request, obj, form, change):
        if not request.user.has_perm('info.add_branch'):
            member = get_bind_member(request.user)
            branches = map(int, request.POST['branch'].split(' '))
            if member is None or member.branch.id not in branches:
                if self.org_obj is None:
                    messages.warning(request, '您添加了其他党支部的活动。')
                else:
                    messages.error(request, '修改失败，您不是%s的书记。' %
                                   '或'.join([str(b) for b in obj.branch.all()]))
                    return
        obj.save()


@admin.register(TakePartIn)
class CreditAdmin(ImportExportModelAdmin):
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

    def get_queryset(self, request):
        if not request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            m = get_bind_member(request.user)
            if m is None:
                return self.model.objects.none()
            if request.user.has_perm('info.add_member'):  # 支书
                colleges = Member.objects.filter(branch=m.branch)  # 找到该model 里该用户创建的数据
                return self.model.objects.filter(member__in=colleges)
            return self.model.objects.filter(member=m)  # 普通成员
        return self.model.objects.all()

    def save_model(self, request, obj, form, change):
        obj = self.new_obj
        if not request.user.has_perm('info.add_branch'):
            member = get_bind_member(request.user)
            branches = obj.activity.branch.all()
            if member is None or member.branch not in branches and obj.credit != obj.activity.credit:
                obj.credit = obj.activity.credit
        obj.save()

    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['credit']
        else:
            return []

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            if not request.user.has_perm('info.add_branch'):
                member = get_bind_member(request.user)
                branches = obj.activity.branch.all()
                if member is None or member.branch not in branches:
                    return ['member', 'activity', 'credit']
            return ['member', 'activity']
