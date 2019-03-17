from xadmin.plugins.actions import BaseActionView
from datetime import datetime
from django.contrib import messages


class ActivistAction(BaseActionView):
    action_name = u'add_activist'
    model_perm = 'add'
    description = '确定为入党积极分子'

    def do_action(self, queryset):
        success = []
        for obj in queryset:
            if obj.activist_date is None:
                obj.activist_date = datetime.now()
                obj.save()
                success.append(obj.name)
        messages.success(self.request, '成功确定' + ','.join(success) + '为入党积极分子。')


class KeyPersonAction(BaseActionView):
    action_name = u'add_key_person'
    model_perm = 'add'
    description = '确定为重点发展对象'

    def do_action(self, queryset):
        success = []
        for obj in queryset:
            if obj.key_develop_person_date is None:
                obj.key_develop_person_date = datetime.now()
                obj.save()
                success.append(obj.name)
        messages.success(self.request, '成功确定' + ','.join(success) + '为重点发展对象。')


class PrememberAction(BaseActionView):
    action_name = u'add_premember'
    model_perm = 'add'
    description = '确定为预备党员'

    def do_action(self, queryset):
        success = []
        for obj in queryset:
            if obj.first_branch_conference is None:
                obj.first_branch_conference = datetime.now()
                obj.save()
                success.append(obj.name)
        messages.success(self.request, '成功确定' + ','.join(success) + '为预备党员。')


class MemberAction(BaseActionView):
    action_name = u'add_member'
    model_perm = 'add'
    description = '确定为正式党员'

    def do_action(self, queryset):
        success = []
        for obj in queryset:
            if obj.second_branch_conference is None:
                obj.second_branch_conference = datetime.now()
                obj.save()
                success.append(obj.name)
        messages.success(self.request, '成功确定' + ','.join(success) + '为正式党员。')                