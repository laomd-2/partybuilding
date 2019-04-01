import datetime
from django.contrib.auth.models import Group

from info.models import Member


def get_end_time(days):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days)
    return now - delta, now.month


def group_by_branch(appers):
    groups = dict()
    for apper in appers:
        groups.setdefault(apper.branch, [])
        groups[apper.branch].append(apper)
    return groups


def get_branch_managers():
    group = Group.objects.get(name='党支部管理员')
    managers = group.user_set.all()
    branch_managers = dict()
    for manager in managers:
        branch = Member.objects.get(netid=int(manager.username)).branch
        if branch.id != 1:
            continue
        branch_managers.setdefault(branch, [])
        branch_managers[branch].append(manager)
    return branch_managers
