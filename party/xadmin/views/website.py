from __future__ import absolute_import
from django.utils.translation import ugettext as _
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView as login
from django.contrib.auth.views import LogoutView as logout
from django.http import HttpResponse
from .base import BaseAdminView, filter_hook
from .dashboard import Dashboard
from xadmin.forms import AdminAuthenticationForm
from xadmin.models import UserSettings
from xadmin.layout import FormHelper
from notice.admin import *
from notice.util import verbose_name, queryset


class IndexView(Dashboard):
    title = _("Main Dashboard")
    icon = "fa fa-dashboard"

    def get_page_id(self):
        return 'home'

    def get_context(self):
        context = super(IndexView, self).get_context()
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


class UserSettingView(BaseAdminView):

    @never_cache
    def post(self, request):
        key = request.POST['key']
        val = request.POST['value']
        us, created = UserSettings.objects.get_or_create(
            user=self.user, key=key)
        us.value = val
        us.save()
        return HttpResponse('')


class LoginView(BaseAdminView):
    title = _("Please Login")
    login_form = None
    login_template = None

    @filter_hook
    def update_params(self, defaults):
        pass

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        context.update({
            'title': self.title,
            'helper': helper,
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        })
        defaults = {
            'extra_context': context,
            # 'current_app': self.admin_site.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'xadmin/views/login.html',
        }
        self.update_params(defaults)
        # return login(request, **defaults)
        return login.as_view(**defaults)(request)

    @never_cache
    def post(self, request, *args, **kwargs):
        return self.get(request)


class LogoutView(BaseAdminView):
    logout_template = None
    need_site_permission = False

    @filter_hook
    def update_params(self, defaults):
        pass

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        defaults = {
            'extra_context': context,
            # 'current_app': self.admin_site.name,
            'template_name': self.logout_template or 'xadmin/views/logged_out.html',
        }
        if self.logout_template is not None:
            defaults['template_name'] = self.logout_template

        self.update_params(defaults)
        # return logout(request, **defaults)
        return logout.as_view(**defaults)(request)

    @never_cache
    def post(self, request, *args, **kwargs):
        return self.get(request)
