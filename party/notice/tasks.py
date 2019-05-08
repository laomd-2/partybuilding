from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView
from info.util import *
from info.models import get_branch_managers
from notice.admin import *
from notice.views import queryset
from notice.util import send_email_to_appliers, send_email_to_managers


class EmailView(TemplateView):
    table_mapping = dict([(model.__name__.lower(), model)
                        for model in [FirstTalk, Activist, KeyDevelop, PreMember, FullMember]])
    def post(self, request, table):
        model = self.table_mapping.get(table)
        if model is not None:
            return self.send_email(request, model, model.verbose_name, model.verbose_name, model.phase)
        return HttpResponseNotFound('NOT FOUND')

    @staticmethod
    def send_email(request, model, manager_title, member_title, phase):
        if not is_school_admin(request.user):
            raise PermissionDenied
        groups = group_by_branch(queryset(request, model))
        branch_managers = get_branch_managers()
        fields = model.fields
        success = []
        for branch, appers in groups.items():
            if branch in branch_managers and branch == 85:
                send_email_to_managers(branch_managers[branch], manager_title, appers,
                                    fields, phase)
                # send_email_to_appliers(member_title, appers, fields)
                success.append(branch.branch_name)
        if success:
            messages.success(request, '%s：已向%s支书发送邮件！' % (manager_title, ','.join(success)))
        return HttpResponseRedirect('/')
