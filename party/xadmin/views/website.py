from __future__ import absolute_import

from collections import OrderedDict

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
from notice.models import *
from notice.views import queryset


class IndexView(Dashboard):
    title = _("Main Dashboard")
    icon = "fa fa-dashboard"

    def get_page_id(self):
        return 'home'

    def get_context(self):
        context = super(IndexView, self).get_context()
        affairs = []
        for model in [FirstTalk, Activist, KeyDevelop, PreMember, FullMember]:
            query = queryset(self.request, model)
            if query:
                if hasattr(model, 'fields'):
                    fields, header = model.fields()
                else:
                    fields = [field.name for field in model._meta.fields]
                    header = [model._meta.get_field(field).verbose_name for field in fields]
                result = [header]
                for q in query:
                    result.append([getattr(q, field) for field in fields])
                affairs.append([model._meta.verbose_name, result])
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
