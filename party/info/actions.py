from xadmin.plugins.actions import BaseActionView
from datetime import datetime
from django.contrib import messages


class ActivistAction(BaseActionView):
    action_name = u'add_activist'
    model_perm = 'add'
    description = '确定为入党积极分子'

    def do_action(self, queryset):
        queryset.filter(activist_date__isnull=True).update(activist_date=datetime.now())


class KeyPersonAction(BaseActionView):
    action_name = u'add_key_person'
    model_perm = 'add'
    description = '确定为重点发展对象'

    def do_action(self, queryset):
        queryset.filter(key_develop_person_date__isnull=True) \
            .update(key_develop_person_date=datetime.now())


class PrememberAction(BaseActionView):
    action_name = u'add_premember'
    model_perm = 'add'
    description = '确定为预备党员'

    def do_action(self, queryset):
        queryset.filter(first_branch_conference__isnull=True) \
            .update(first_branch_conference=datetime.now())


class MemberAction(BaseActionView):
    action_name = u'add_member'
    model_perm = 'add'
    description = '确定为正式党员'

    def do_action(self, queryset):
        queryset.filter(second_branch_conference__isnull=True) \
            .update(second_branch_conference=datetime.now())
