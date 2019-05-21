from django.contrib import messages
from django.db.models import F
# from teaching.models import TakePartIn
from new_party.admin import *
from .util import *
from info.resources import MemberResource
from common.rules import *
from common.utils import get_old
# from teaching.util import get_detail_chart as get_credit_chart
from .models import *
from .forms import InfoForm
# from .actions import *


class SchoolAdmin(BaseModelAdmin):
    list_display = ['name']
    list_exclude = ['id']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15


class BranchAdmin(BaseModelAdmin):
    my_export = True
    # actions = [MergeBranchAction]
    list_display = ['branch_name', 'get_leaders',
                    'num_members', 'num_full_members',
                    'num_pre_members', 'num_key',
                    'num_activist', 'num_application', 'date_create']
    button_pull_left = True
    show_charts = True
    list_display_links = ['branch_name']
    model_icon = 'fa fa-flag'
    # list_per_page = 15

    def get_search_fields(self, request):
        if is_school_admin(request.user):
            return ['branch_name']
        return []

    # @property
    # def detail_charts(self):
    #     charts = get_detail_chart(request)
    #     credit_charts = get_credit_chart(request, TakePartIn)
    #     if credit_charts:
    #         charts.update(credit_charts)
    #     return charts

    # @property
    # def list_charts(self):
    #     return get_list_chart(request)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['school']

    def get_queryset(self, request):
        qs = self.model.objects.select_related('school')
        if request.user.is_superuser:
            return qs.all()
        if is_school_manager(request.user):  # 判断是否是党辅
            school = int(request.user.username[0])
            return School.objects.get(id=school).branch_set.all()
        else:
            member = request.user.member
            if member is None:
                return qs.none()
            return qs.filter(id=member['branch_id'])

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            if is_branch_manager(request.user):
                m = request.user.member
                return m is not None and m['branch_id'] == obj.id
        return False

    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj):
            if is_school_admin(request.user) or obj is None:
                return True
            m = request.user.member
            return m is not None and m['branch_id'] == obj.id
        return False

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (obj is None or obj.id != 106)


fields_, phases = Member.get_phases()


class MemberBaseAdmin(IEModelAdmin):
    form = InfoForm
    resource_class = MemberResource
    list_display = fields_[:4] + ['gender', 'application_date', 'activist_date',
                                  'key_develop_person_date', 'first_branch_conference',
                                  'second_branch_conference']
    list_exclude = ['phase']
    list_display_links = ('netid',)
    button_pull_left = True

    @property
    def num_fixed_cols(self):
        res = 0
        for fix in ['branch', 'netid', 'name']:
            if fix in self.list_display:
                res += 1
        return res

    ordering = ['branch', 'second_branch_conference',
                'first_branch_conference',
                'key_develop_person_date',
                'activist_date', 'netid']
    # wizard_form_list = phases.items()

    # form_layout = (
    #     Main(
    #         *[Fieldset((('阶段%d：' % i) if i else '') + k, *v) for i, (k, v) in enumerate(phases.items())]
    #     ),
    #     Side(
    #         Fieldset('关系转出', 'out_type', 'out_date', 'out_place'),
    #         Fieldset('其他信息', 'remarks')
    #     )
    # )

    def get_search_fields(self, request):
        if is_admin(request.user):
            return ['netid', 'name']
        return []

    def get_list_filter(self, request):
        if is_admin(request.user):
            general = [
                'phase',
                'first_talk_date',
            ]
            if is_branch_manager(request.user):
                return general
            else:
                return ['branch'] + general
        return []

    # @property
    # def list_editable(self):
    #     if is_admin(request.user):
    #         return [f for f in fields_ if f != 'netid']
    #     if is_member(request.user):  # 普通成员
    #         return phases['基本信息'][2:]
    #     return []

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        res = ['netid']
        if not is_school_admin(request.user):
            res.append('branch')
            if is_member(request.user):  # 普通成员
                m = request.user.member
                if m is None or m['netid'] != obj.netid:
                    return fields_
                for k, v in phases.items():
                    if k != '基本信息':
                        res += v
                res.extend(['out_date', 'out_place', 'remarks'])
        return res

    def get_queryset(self, request):
        queryset = get_visuable_members(self.model, request.user)
        orders = []
        for o in self.ordering:
            if o[0] == '-':
                orders.append(F(o[1:]).desc(nulls_last=True))
            else:
                orders.append(F(o).asc(nulls_last=True))
        return queryset.order_by(*orders)

    def save_model(self, request, obj, form, change):
        if not is_school_admin(request.user):
            member = request.user.member
            if member is None or obj.branch_id != member['branch_id']:
                old = get_old(obj)
                messages.error(request, '%s失败，您没有此权限。' %
                                        '添加' if old is None else '修改')
                return
        obj.save()

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if obj is None or request.user.is_superuser:
                return True
            else:
                m = request.user.member
                if m is not None:
                    if is_branch_admin(request.user):
                        return m['branch_id'] == obj.branch_id
                    elif is_member(request.user):
                        return m['netid'] == obj.netid
                elif is_school_manager(request.user):
                    return obj.branch.school_id == int(request.user.username[0])
        return False


class DependencyAdmin(BaseModelAdmin):
    list_display = ['from_1', 'to', 'days', 'scope']
    list_exclude = ['id']
    list_editable = ['days', 'scope']
    model_icon = 'fa fa-link'

    def get_list_display_links(self, request, list_display):
        if 'from_1' in list_display and is_school_admin(request.user):
            return ['from_1']
        else:
            return [None, ]


class MemberAdmin(MemberBaseAdmin):
    model_icon = 'fa fa-info'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'branch':
            kwargs["queryset"] = get_visual_branch(request.user)
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class OldMemberAdmin(MemberBaseAdmin):
    model_icon = 'fa fa-info-circle'


site.register(School, SchoolAdmin)
site.register(Branch, BranchAdmin)
site.register(Dependency, DependencyAdmin)
site.register(Member, MemberAdmin)
site.register(OldMember, OldMemberAdmin)
