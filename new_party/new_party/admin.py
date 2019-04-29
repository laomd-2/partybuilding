from django.contrib import admin, messages

from common.base import wrap
from common.rules import is_school_admin
from notice.admin import *
from notice.views import queryset


class MyAdminSite(admin.AdminSite):
    site_title = '计二党建系统'
    site_header = site_title

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        affairs = []
        for model in [FirstTalk, Activist, KeyDevelop, LearningClass, PreMember, FullMember]:
            query = queryset(request, model)
            if query:
                fields = model.fields
                header = verbose_name(fields)
                result = [header]
                for q in query:
                    result.append([wrap(getattr(q, field)) for field in fields])
                affairs.append([model.__name__.lower(), model.verbose_name, result])
        extra_context['affairs'] = affairs
        extra_context['can_send_email'] = is_school_admin(request.user)
        return super(MyAdminSite, self).index(request, extra_context)