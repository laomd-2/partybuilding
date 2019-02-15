from django.contrib import messages
import xadmin
from user.models import get_bind_member
from xadmin.layout import Main, Fieldset
from .models import School, Branch, Member, Dependency
from .resources import MemberResource


@xadmin.sites.register(School)
class SchoolAdmin(object):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    model_icon = 'fa fa-university'
    list_per_page = 15
    list_editable = list_display[1:]


@xadmin.sites.register(Branch)
class BranchAdmin(object):
    list_display = ['id', 'school', 'branch_name']
    list_display_links = ['branch_name']
    search_fields = ['branch_name']
    list_filter = ['branch_name']
    model_icon = 'fa fa-user'
    list_per_page = 15
    list_editable = list_display[1:]

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            member = get_bind_member(self.request.user)
            if member is None:
                return self.model.objects.none()
            else:
                return self.model.objects.filter(school=member.branch.school)
        return self.model.objects.all()


@xadmin.sites.register(Dependency)
class DependencyAdmin(object):
    list_display = ['from_1', 'to', 'days']
    list_editable = list_display

    def get_list_display_links(self):
        if self.request.user.has_perm('info.add_branch'):
            return ['from_1']
        else:
            return [None, ]


@xadmin.sites.register(Member)
class MemberAdmin(object):
    import_export_args = {'import_resource_class': MemberResource}

    fields = [field.name for field in Member._meta.fields]
    list_display = fields[1:6]
    search_fields = ['netid', 'name']
    list_filter = ['name', 'application_date',
                   'activist_date',
                   'key_develop_person_date',
                   'first_branch_conference',
                   'second_branch_conference']
    model_icon = 'fa fa-info'
    list_per_page = 10
    list_editable = list_display[1:]
    # relfield_style = 'fk_ajax'

    phases = dict()
    phases['基本信息'] = fields[:10]
    phases['阶段1：入党考察'] = fields[10:19]
    phases['阶段2：预备党员'] = fields[19:28]
    phases['阶段3：正式党员'] = fields[28:]
    wizard_form_list = phases.items()
    form_layout = (
        Main(
            *[Fieldset(k, *v) for k, v in wizard_form_list]
        )
    )

    def get_readonly_fields(self):
        if not self.request.user.has_perm('info.add_member'):  # 普通成员
            res = ['branch', 'netid'] + self.phases['阶段1：入党考察'] + \
                  self.phases['阶段2：预备党员'] + self.phases['阶段3：正式党员']
            res.remove('youth_league_date')
            res.remove('constitution_group_date')
            return res
        return []

    def queryset(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            member = get_bind_member(self.request.user)
            if member is None:
                qs = self.model.objects.none()
            else:
                if self.request.user.has_perm('info.add_member'):  # 支书
                    qs = self.model.objects.filter(branch=member.branch)
                else:
                    qs = self.model.objects.filter(netid=member.netid, branch=member.branch)  # 普通成员
        else:
            qs = self.model.objects.all()
        return qs

    @staticmethod
    def check(obj):
        errors = []
        for dep in Dependency.objects.all():
            from_ = getattr(obj, dep.from_1)
            to = getattr(obj, dep.to)
            if from_ and to:
                delta = to - from_
                if delta.days < dep.days:
                    errors.append((dep.from_1, dep.to, delta.days, dep.days))
        return errors

    def save_models(self):
        if hasattr(self, 'new_obj'):
            obj = self.new_obj
            errors = self.check(obj)
            if errors and self.org_obj is None:
                for e in errors:
                    messages.error(self.request,
                                   "%s到%s需要%d天，而%s只用了%d天。"
                                   % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
                                      Member._meta.get_field(e[1]).verbose_name.strip('时间'),
                                      e[3], obj, e[2]))
                obj.delete()
            else:
                if self.request.user.is_superuser:
                    obj.save()
                else:
                    member = get_bind_member(self.request.user)
                    if member is None or obj.branch != member.branch:
                        messages.error(self.request, '%s失败，您不是%s的书记。' %
                                       ('添加' if self.org_obj is None else '修改', obj.branch))
                        if self.org_obj is None:
                            obj.delete()
                    else:
                        obj.save()

    @property
    def datas(self):
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            qs = self.model.objects.all()
        else:
            member = get_bind_member(self.request.user)
            if member is None:
                qs = self.model.objects.none()
            else:
                qs = self.model.objects.filter(branch=member.branch)
        grades = dict()
        identities = ['application_date',
                      'activist_date',
                      'key_develop_person_date',
                      'first_branch_conference',
                      'second_branch_conference']
        identities.reverse()
        for member in qs:
            grade = member.netid[:2]
            grades.setdefault(grade, [0, 0, 0, 0, 0])
            for i, identity in enumerate(identities):
                if getattr(member, identity) is not None:
                    grades[grade][i] += 1
                    break
        xadix = list(grades.keys())
        xadix.sort(reverse=True)
        return xadix, [grades[k] for k in xadix]
