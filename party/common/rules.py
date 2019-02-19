import rules
from django.contrib.auth.models import Group


@rules.predicate
def is_branch_manager(user):
    g = Group.objects.get(name='支书')
    return g in user.groups.all()


@rules.predicate
def is_school_manager(user):
    g = Group.objects.get(name='党辅')
    return g in user.groups.all()


@rules.predicate
def is_member(user):
    g = Group.objects.get(name='普通成员')
    return g in user.groups.all()


is_school_admin = is_school_manager | rules.is_superuser
is_branch_admin = is_branch_manager | rules.is_superuser
is_admin = is_branch_admin | is_school_admin
