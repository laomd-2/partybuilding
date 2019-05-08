from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView
from django.core import mail
from info.util import *
from info.models import get_branch_managers
from notice.admin import *
from notice.views import queryset
from notice.util import make_email_to_appliers, make_email_to_managers


class EmailView(TemplateView):
    table_mapping = dict([(model.__name__.lower(), model)
                          for model in [FirstTalk, Activist, KeyDevelop, LearningClass, PreMember, FullMember]])

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
        mails = []
        for branch, appers in groups.items():
            appers = list(appers)
            if branch in branch_managers:
                mails.append(make_email_to_managers(branch_managers[branch], manager_title, appers,
                                                    fields, phase))
                success.append(appers[0]['branch_name'])
            mails.extend(make_email_to_appliers(member_title, appers, fields))
        connection = mail.get_connection()  # Use default email connection
        connection.fail_silently = True
        cnt = connection.send_messages(mails)
        messages.success(request, '%s：成功发送%d封邮件！' % (manager_title, cnt))
        return HttpResponseRedirect('#')
