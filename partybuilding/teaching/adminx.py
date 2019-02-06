import xadmin
from info.models import Member
from .models import Credit
from .resources import CreditResource


class CreditAdmin(object):
    import_export_args = {'import_resource_class': CreditResource}

    list_display = [field.name for field in Credit._meta.get_fields()][1:]
    list_display_links = ('netid', )
    search_fields = ['date', 'netid__name', 'netid__netid']

    # model_icon = 'fa fa-info'
    list_per_page = 15
    aggregate_fields = {"credit": "sum"}

    @property
    def list_filter(self):
        if self.request.user.has_perm('teaching.change_credit'):  # 支书
            return ['date', 'activity']
        return ['date']

    @property
    def list_editable(self):
        if self.request.user.has_perm('teaching.change_credit'):  # 支书
            return ['credit']
        return []

    def get_readonly_fields(self):
        if self.request.user.has_perm('teaching.change_credit'):  # 支书
            return []
        return self.list_display

    def queryset(self):
        if not self.request.user.is_superuser:  # 判断是否是超级用户
            member = Member.objects.get(netid=self.request.user)
            if self.request.user.has_perm('teaching.change_credit'):   # 支书
                colleages = Member.objects.filter(branch_name=member.branch_name)
                return self.model.objects.filter(netid__in=[c.netid for c in colleages])
            return self.model.objects.filter(netid=member.netid)    # 普通成员
        return self.model.objects.all()


xadmin.site.register(Credit, CreditAdmin)
