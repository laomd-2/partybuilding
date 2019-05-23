from django.apps import apps
from django.contrib.admin import AdminSite, ModelAdmin
from django.urls import reverse, NoReverseMatch
from django.utils.text import capfirst
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin
from xxadmin.forms import DateCheckModelForm
from notice.admin import *


class MyAdminSite(AdminSite):
    index_title = '主页'
    site_header = '数据科学与计算机学院学生党建系统'
    site_title = site_header

    def index(self, request, extra_context=None):
        super().index(request, extra_context)
        extra_context = extra_context or {}
        affairs = []
        plans = []
        today = datetime.date.today()
        for model in [FirstTalk, Activist, KeyDevelop, LearningClass, PreMember, FullMember]:
            query = queryset(request, model)
            num_plan = len(query)
            if num_plan > 0:
                fields = model.fields
                headers = verbose_name(fields)
                results = [[m[f] for f in fields] for m in query]
                beian_template = model.beian_template.split('/')[-1]
                if beian_template.endswith('.docx'):
                    beian_template = beian_template[:-5]
                plans.append((model.verbose_name, num_plan, model.__name__.lower(), headers, results, beian_template))
                daiban = model.check(today, query)
                num_daiban = len(daiban)
                if num_daiban > 0:
                    affairs.append((model.phase, num_daiban,
                                    '_p_netid__in=' + ','.join(map(lambda x: str(x), daiban)),
                                    model.fields))
        extra_context['can_beian'] = is_admin(request.user)
        extra_context['plans'] = plans
        extra_context['affairs'] = affairs
        return super().index(request, extra_context)

    def each_context(self, request):
        context = super().each_context(request)
        context['app_list'] = context['available_apps']
        return context

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            icon = ''
            if hasattr(model_admin, 'model_icon'):
                icon = model_admin.model_icon
            model_dict = {
                'icon': icon,
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
            }
            if perms.get('change') or perms.get('view'):
                model_dict['view_only'] = not perms.get('change')
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict


site = MyAdminSite()


class AdminMixin:
    form = DateCheckModelForm
    list_export = []
    list_exclude = ['id']
    list_per_page = 15
    actions_on_bottom = True
    actions_on_top = False
    formats = base_formats.DEFAULT_FORMATS[2:3]

    def changelist_view(self, request, extra_context=None):
        model_fields = []
        list_display = self.get_list_display(request)
        all_fields = [f.name for f in self.opts.fields]
        for f in self.list_display:
            if f not in all_fields:
                all_fields.append(f)
        field_verbose = verbose_name(all_fields, self.model)
        for f, v in zip(all_fields, field_verbose):
            if f not in self.list_exclude:
                model_fields.append((v, f in list_display, f))
        extra_context = extra_context or {}
        extra_context['model_fields'] = model_fields
        return super().changelist_view(request, extra_context)

    def get_list_display(self, request):
        return request.POST.getlist('list_display') or self.list_display


class BaseModelAdmin(AdminMixin, ModelAdmin):
    pass


class IEModelAdmin(AdminMixin, ImportExportModelAdmin):
    pass
