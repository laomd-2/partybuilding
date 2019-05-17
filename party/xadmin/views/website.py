from __future__ import absolute_import

from collections import OrderedDict

from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView as login
from django.contrib.auth.views import LogoutView as logout
from django.http import HttpResponse

from common.base import wrap
from common.rules import is_school_admin
from .base import BaseAdminView, filter_hook
from .dashboard import Dashboard
from xadmin.forms import AdminAuthenticationForm
from xadmin.models import UserSettings
from xadmin.layout import FormHelper
from notice.admin import *
from notice.util import verbose_name
from notice.views import queryset


class IndexView(Dashboard):
    title = _("Main Dashboard")
    icon = "fa fa-dashboard"

    def get_page_id(self):
        return 'home'

    def get_context(self):
        context = super(IndexView, self).get_context()
        affairs = []
        deffers = dict()
        for model in [FirstTalk, Activist, KeyDevelop, LearningClass, PreMember, FullMember]:
            query = queryset(self.request, model)
            if query:
                fields = model.fields
                header = verbose_name(fields)
                result = [header]
                for q in query:
                    q['branch_id'] = q['branch_name']
                    result.append([wrap(q[field]) for field in fields])
                beian_tile = model.beian_template.split('/')[-1]
                beian_tile = beian_tile[beian_tile.find('：') + 1: beian_tile.rfind('.')]
                affairs.append([model.__name__.lower(), model.verbose_name, result, beian_tile])

                if is_admin(self.request.user):
                    today = datetime.datetime.now().date()
                    deffer = model.check(today, query)
                    if deffer:
                        rows = [header]
                        for q in deffer:
                            rows.append([wrap(q[field]) for field in fields])
                        deffers[model.phase] = rows
                    graduation = list(get_graduation(self.request))
                    if graduation:
                        for g in graduation:
                            g['branch_id'] = g['branch_name']
                            del g['branch_name']
                        header = verbose_name(graduation[0].keys())
                        context['graduation'] = [header] + [list(map(wrap, g.values())) for g in graduation]

        context['deffers'] = deffers
        context['affairs'] = affairs
        context['can_send_email'] = is_school_admin(self.request.user)
        context['can_beian'] = is_admin(self.request.user)
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
