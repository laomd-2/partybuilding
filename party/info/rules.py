import rules
from django.contrib.auth.models import Group


@rules.predicate
def is_branch_manager(user):
    g = Group.objects.get(name='支书')
    return g in user.groups.all()


@rules.predicate
def is_school_admin(user):
    g = Group.objects.get(name='党辅')
    return g in user.groups.all()


@rules.predicate
def is_member(user):
    g = Group.objects.get(name='普通成员')
    return g in user.groups.all()

#
# rules.add_rule('can_view_member', is_school_admin | is_branch_manager | is_member)
# rules.add_rule('can_delete_member', is_branch_manager)
# rules.add_rule('can_change_member', is_branch_manager)
#
# # 设置Permissions
#
# rules.add_perm('info.view_member', is_school_admin | is_branch_manager | is_member)
# rules.add_perm('info.delete_member', is_branch_manager)
# rules.add_perm('info.add_member', is_branch_manager)
# rules.add_perm('info.change_member', is_branch_manager)
