from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from info.resources import MemberResource
from user.models import get_bind_member
from .models import School, Branch, Member, Dependency


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'school', 'branch_name']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['school__name']
    model_icon = 'fa fa-user'
    list_per_page = 15

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('info.add_branch'):
            member = get_bind_member(request.user)
            if member is None or member.branch != obj:
                return ['school', 'branch_name', 'date_create']
            return ['school']
        return []

    def get_queryset(self, request, obj=None):
        if request.user.is_superuser:
            return self.model.objects.all()
        if request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            school = int(request.user.username[0])
            return self.model.objects.filter(school__id=school)
        else:
            member = get_bind_member(request.user)
            if member is None:
                return self.model.objects.none()
            else:
                return self.model.objects.filter(school=member.branch.school)


@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource

    fields = [field.name for field in Member._meta.fields]
    list_display = fields[1:5] + ['phone_number', 'major_in']

    model_icon = 'fa fa-info'
    list_per_page = 15
    # list_editable = list_display[1:]
    # relfield_style = 'fk_ajax'

    phases = dict()
    phases['基本信息'] = fields[:10]
    phases['阶段1：入党考察'] = fields[10:19]
    phases['阶段2：预备党员'] = fields[19:28]
    phases['阶段3：正式党员'] = fields[28:]
    wizard_form_list = phases.items()

    # form_layout = (
    #     Main(
    #         *[Fieldset(k, *v) for k, v in wizard_form_list]
    #     )
    # )

    def get_search_fields(self, request):
        if request.user.has_perm('info.add_member') or \
                request.user.has_perm('info.add_branch'):
            return ['netid', 'name']
        return []

    def get_list_filter(self, request):
        if request.user.has_perm('info.add_member') or \
                request.user.has_perm('info.add_branch'):
            return ['application_date',
                    'activist_date',
                    'key_develop_person_date',
                    'first_branch_conference',
                    'second_branch_conference']
        return []

    def get_readonly_fields(self, request, obj=None):
        if not request.user.has_perm('info.add_member'):  # 普通成员
            res = ['branch', 'netid'] + self.phases['阶段1：入党考察'] + \
                  self.phases['阶段2：预备党员'] + self.phases['阶段3：正式党员']
            res.remove('youth_league_date')
            res.remove('constitution_group_date')
            return res
        return []

    def get_queryset(self, request, obj=None):
        if not request.user.has_perm('info.add_branch'):  # 判断是否是党辅
            member = get_bind_member(request.user)
            if member is None:
                qs = self.model.objects.none()
            else:
                if request.user.has_perm('info.add_member'):  # 支书
                    qs = self.model.objects.filter(branch=member.branch)
                else:
                    qs = self.model.objects.filter(netid=member.netid, branch=member.branch)  # 普通成员
        else:
            qs = self.model.objects.all()
        return qs

    @staticmethod
    def check_dep(obj):
        errors = []
        for dep in Dependency.objects.all():
            from_ = getattr(obj, dep.from_1)
            to = getattr(obj, dep.to)
            if from_ and to:
                delta = to - from_
                if delta.days < dep.days:
                    errors.append((dep.from_1, dep.to, delta.days, dep.days))
        return errors

    def save_model(self, request, obj, form, change):
        if obj is not None:
            errors = self.check_dep(obj)
            for e in errors:
                messages.error(request,
                               "%s到%s需要%d天，而%s只用了%d天。"
                               % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
                                  Member._meta.get_field(e[1]).verbose_name.strip('时间'),
                                  e[3], obj, e[2]))
                break
            else:
                if request.user.is_superuser:
                    obj.save()
                else:
                    member = get_bind_member(request.user)
                    if member is None or obj.branch != member.branch:
                        messages.error(request, '%s失败，您不是%s的书记。' %
                                       ('添加' if obj is None else '修改', obj.branch))
                    else:
                        obj.save()


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ['from_1', 'to', 'days']
    list_editable = ['days']

    def get_list_display_links(self, request, obj=None):
        if request.user.has_perm('info.add_branch'):
            return ['from_1']
        else:
            return [None, ]
