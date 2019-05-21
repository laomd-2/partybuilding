from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.views.generic import TemplateView, ListView
from notice.admin import *
from notice.util import verbose_name

GroupAdmin.model_icon = 'fa fa-users'


class BaseView(TemplateView):
    def get_context_data(self, request, **kwargs):
        context = super().get_context_data()
        context['app_list'] = admin.site.get_app_list(request)
        registry = admin.site._registry
        for app in context['app_list']:
            for model in app['models']:
                model_class = apps.get_registered_model(app['app_label'], model['object_name'].lower())
                admin_view = registry[model_class]
                model['icon'] = admin_view.model_icon
        context['user'] = request.user
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)


class IndexView(BaseView):
    template_name = 'index.html'

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(request)
        context['title'] = '主页面'
        affairs = []
        plans = []
        today = datetime.date.today()
        for model in [FirstTalk, Activist, KeyDevelop, LearningClass, PreMember, FullMember]:
            query = queryset(self.request, model)
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
        context['can_beian'] = is_admin(self.request.user)
        context['plans'] = plans
        context['affairs'] = affairs
        return context


class ListAdminView(ListView):
    # template_name =
    pass