from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.forms import modelform_factory
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from info.models import Dependency
from info.util import field_range
from xadmin.defs import ACTION_CHECKBOX_NAME
from xadmin.dutils import force_text
from xadmin.layout import FormHelper, Layout, Fieldset, Container, Col
from xadmin.plugins.batch import BaseActionView, ChangeFieldWidgetWrapper, BATCH_CHECKBOX_NAME
from datetime import date, timedelta

from xadmin.util import model_ngettext
from xadmin.views import ModelFormAdminView, filter_hook


class MyBatchChangeAction(BaseActionView):
    batch_change_form_template = 'batch_change_form.html'
    last_date = ''
    phase = ''

    @property
    def related_fields(self):
        return field_range(self.last_date, self.phase)

    @filter_hook
    def get_media(self):
        media = super().get_media()
        media = media + self.form_obj.media + self.vendor(
            'xadmin.page.form.js', 'xadmin.form.css')
        return media

    def get_change_form(self, is_post, fields):
        edit_view = self.get_model_view(ModelFormAdminView, self.model)

        def formfield_for_dbfield(db_field, **kwargs):
            formfield = edit_view.formfield_for_dbfield(db_field, required=is_post, **kwargs)
            formfield.widget = ChangeFieldWidgetWrapper(formfield.widget)
            return formfield

        defaults = {
            "form": edit_view.form,
            "fields": fields,
            "formfield_callback": formfield_for_dbfield,
        }
        return modelform_factory(self.model, **defaults)

    def get_context(self):
        context = super().get_context() or {}
        context['action_name'] = self.action_name
        return context
    
    def filter_valid(self, queryset, field, value):
        try:
            days = Dependency.objects.get(Q(scope=0) | Q(scope=1), from_1=self.last_date, to=self.phase).days
            end = value - timedelta(days=days)
            queryset = queryset.filter(**{
                self.last_date + "__lt": end
            })
        except Exception as e:
            print(e)
            pass
        return queryset

    def change_models(self, queryset, cleaned_data):
        data = {}
        fields = self.opts.fields + self.opts.many_to_many
        for f in fields:
            if not f.editable or isinstance(f, models.AutoField) \
                    or not f.name in cleaned_data:
                continue
            data[f] = cleaned_data[f.name]
            if f.name == self.phase:
                queryset = self.filter_valid(queryset, f.name, data[f])

        n = 0
        for obj in queryset:
            for f, v in data.items():
                f.save_form_data(obj, v)
            obj.save()
            n += 1
        if n:
            self.message_user(_("Successfully change %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, 'success')
        else:
            messages.warning(self.request, '您填的日期不符合流程依赖中的时间间隔。')
    
    def do_action(self, queryset):
        if not self.has_add_permission():
            raise PermissionDenied
        queryset = self.filter_valid(queryset.filter(is_sysu=True, **{
            self.phase + "__isnull": True
        }), self.phase, date.today())
        if queryset.exists():
            related_fields = self.related_fields
            change_fields = [f for f in self.request.POST.getlist(BATCH_CHECKBOX_NAME) if f in related_fields]
            if change_fields and self.request.POST.get('post'):
                self.form_obj = self.get_change_form(True, change_fields)(
                    data=self.request.POST, files=self.request.FILES)
                if self.form_obj.is_valid():
                    self.change_models(queryset, self.form_obj.cleaned_data)
                    return None
            else:
                self.form_obj = self.get_change_form(False, related_fields)()

            helper = FormHelper()
            helper.form_tag = False
            helper.include_media = False
            helper.add_layout(Layout(Container(Col('full',
                                                   Fieldset("", *self.form_obj.fields.keys(),
                                                            css_class="unsort no_title"), horizontal=True, span=12)
                                               )))
            self.form_obj.helper = helper
            count = len(queryset)
            if count == 1:
                objects_name = force_text(self.opts.verbose_name)
            else:
                objects_name = force_text(self.opts.verbose_name_plural)

            context = self.get_context()
            context.update({
                "title": _("Batch change %s") % objects_name,
                'objects_name': objects_name,
                'form': self.form_obj,
                'queryset': queryset,
                'count': count,
                "opts": self.opts,
                "app_label": self.app_label,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
            })

            return TemplateResponse(self.request, self.batch_change_form_template or
                                    self.get_template_list('views/batch_change_form.html'), context)
        else:
                messages.warning(self.request, '没有符合条件' + self.description + '的人员。')


class ActivistAction(MyBatchChangeAction):
    action_name = u'add_activist'
    model_perm = 'add'
    description = '确定为入党积极分子'
    last_date = 'application_date'

    @property
    def phase(self):
        return 'activist_date'


class KeyPersonAction(MyBatchChangeAction):
    action_name = u'add_key_person'
    model_perm = 'add'
    description = '确定为重点发展对象'
    last_date = 'activist_date'

    @property
    def phase(self):
        return 'key_develop_person_date'


class PrememberAction(MyBatchChangeAction):
    action_name = u'add_premember'
    model_perm = 'add'
    description = '确定为预备党员'
    last_date = 'key_develop_person_date'

    @property
    def phase(self):
        return 'first_branch_conference'


class MemberAction(MyBatchChangeAction):
    action_name = u'add_member'
    model_perm = 'add'
    description = '确定为正式党员'
    last_date = 'first_branch_conference'

    @property
    def phase(self):
        return 'second_branch_conference'


class MergeBranchAction(BaseActionView):
    action_name = u'merge_branch'
    description = '合并所选的 党支部'
    model_perm = 'delete'

    def do_action(self, queryset):
        t_branch = None
        target = None
        cur = -1
        # 迁移的目标支部默认是人数最多的
        for b in queryset:
            num_members = b.member_set.all().count()
            if target is None or num_members > cur:
                target = b.id
                t_branch = b
                cur = num_members
        queryset = queryset.exclude(id=target)
        for branch in queryset:
            # 将旧支部的所有东西迁移到新支部
            branch.member_set.update(branch_id=target)
            branch.oldmember_set.update(branch_id=target)
            branch.note_set.update(branch_id=target)
            branch.rule_set.update(branch_id=target)
            for atv in branch.activity_set.all():
                atv.branch.remove(branch)
                atv.branch.add(t_branch)
                atv.save()
        queryset.delete()
