from django.contrib.admin.utils import get_deleted_objects

from xadmin.plugins.actions import BaseActionView
from datetime import datetime


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


class MergeBranchAction(BaseActionView):
    action_name = u'merge_branch'
    description = '合并所选的 党支部'
    model_perm = 'delete'

    def do_action(self, queryset):
        t_branch = None
        target = None
        cur = -1
        # 迁移的目标支部默认是人数最多的
        for b in queryset:
            num_members = b.member_set.all().count()
            if target is None or num_members > cur:
                target = b.id
                t_branch = b
                cur = num_members
        queryset = queryset.exclude(id=target)
        for branch in queryset:
            # 将旧支部的所有东西迁移到新支部
            branch.member_set.update(branch_id=target)
            branch.oldmember_set.update(branch_id=target)
            branch.note_set.update(branch_id=target)
            branch.rule_set.update(branch_id=target)
            for atv in branch.activity_set.all():
                atv.branch.remove(branch)
                atv.branch.add(t_branch)
                atv.save()
        queryset.delete()
