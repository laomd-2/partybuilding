from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import xadmin
from django.db.models import Q
from info.models import Member
from user.models import get_bind_member
from .models import Activity, TakePartIn
from .resources import CreditResource


@xadmin.sites.register(Activity)
class ActivityAdmin(object):
    # import_export_args = {'import_resource_class': ActivityResource}
    filter_vertical = ('Branch',)  # 关联表
    style_fields = {'branch': 'm2m_transfer'}

    base_list_display = ['name', 'date', 'end_time', 'credit', 'get_branches']

    def get_list_display(self):
        res = self.base_list_display
        if self.request.user.has_perm('info.add_member') or self.request.user.has_perm('info.add_branch'):
            return ['id'] + res
        return res

    list_filter = ['name', 'date', 'end_time', 'credit']
    search_fields = ['name']
    list_per_page = 15
    model_icon = 'fa fa-users'

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            try:
                m = Member.objects.get(netid=self.request.user)
                return self.model.objects.filter(Q(branch__id__contains=m.branch.id) |
                                                 Q(visualable_others=True)).distinct()  # 普通成员
            except ObjectDoesNotExist:
                return self.model.objects.none()
        return self.model.objects.all().distinct()

    def save_models(self):
        obj = self.new_obj
        if not self.request.user.is_superuser:
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
        for t in TakePartIn.objects.filter(activity_id=obj.id):
            t.credit = obj.credit
            t.date = obj.date
            t.end_time = obj.end_time
            t.save()


@xadmin.sites.register(TakePartIn)
class CreditAdmin(object):
    import_export_args = {'import_resource_class': CreditResource}
    search_fields = ['activity__name', 'date', 'member__name']

    list_display = ['member', 'activity', 'date', 'end_time', 'credit']
    list_display_links = (None,)
    list_filter = search_fields
    list_per_page = 15

    model_icon = 'fa fa-bar-chart'
    exclude = ['date', 'credit']
    aggregate_fields = {"credit": "sum"}

    # data_charts = {
    #     "user_count": {'title': "学时统计", "x-field": "date", "y-field": "credit",
    #                    "order": ('date',)
    #                    }
    # }

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            try:
                m = Member.objects.get(netid=self.request.user)
                if self.request.user.has_perm('info.add_member'):  # 支书
                    colleges = Member.objects.filter(branch=m.branch)  # 找到该model 里该用户创建的数据
                    return self.model.objects.filter(member__netid__in=[college.netid for college in colleges])
                return self.model.objects.filter(member__netid=m.netid)  # 普通成员
            except:
                return self.model.objects.filter(member__netid=self.request.user)
        return self.model.objects.all()
