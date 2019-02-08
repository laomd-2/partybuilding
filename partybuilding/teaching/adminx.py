import xadmin

from info.models import Member
from .models import Activity, TakePartIn
from .resources import ActivityResource, CreditResource


@xadmin.sites.register(Activity)
class ActivityAdmin(object):
    import_export_args = {'import_resource_class': ActivityResource}

    filter_vertical = ('Branch',)  # 关联表
    # style_fields = {'branch': 'm2m_transfer'}
    search_fields = ['name', 'date']

    list_display = [field.name for field in Activity._meta.fields]
    list_editable = list_display[1:]
    list_filter = search_fields
    list_per_page = 15

    # model_icon = 'fa fa-info'


@xadmin.sites.register(TakePartIn)
class CreditAdmin(object):
    import_export_args = {'import_resource_class': CreditResource}
    search_fields = ['activity__name', 'activity__date', 'member__name']

    list_display = ['member', 'activity', 'activity_credit']
    list_display_links = (None,)
    list_filter = search_fields
    list_per_page = 15

    # model_icon = 'fa fa-info'

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是超级用户
            try:
                m = Member.objects.get(netid=self.request.user)
                if self.request.user.has_perm('info.add_member'):  # 支书
                    colleges = Member.objects.filter(branch=m.branch)  # 找到该model 里该用户创建的数据
                    return self.model.objects.filter(member__netid__in=[college.netid for college in colleges])
                return self.model.objects.filter(member__netid=m.netid)  # 普通成员
            except:
                return self.model.objects.filter(member__netid=self.request.user)
        return self.model.objects.all()
