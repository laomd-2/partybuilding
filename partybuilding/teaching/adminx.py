from django.core.exceptions import ObjectDoesNotExist

import xadmin
from django.db.models import Q
from info.models import Member
from .models import Activity, TakePartIn
from .resources import CreditResource


@xadmin.sites.register(Activity)
class ActivityAdmin(object):
    # import_export_args = {'import_resource_class': ActivityResource}

    filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}
    search_fields = ['name', 'date']

    list_display = [field.name for field in Activity._meta.fields] + ['get_branches']
    list_display.remove('visualable_others')

    list_editable = list_display[1:]
    list_filter = search_fields
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


@xadmin.sites.register(TakePartIn)
class CreditAdmin(object):
    import_export_args = {'import_resource_class': CreditResource}
    search_fields = ['activity__name', 'activity__date', 'member__name']

    list_display = ['member', 'activity', 'activity_credit']
    list_display_links = (None,)
    list_filter = search_fields
    list_per_page = 15

    model_icon = 'fa fa-bar-chart'

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
