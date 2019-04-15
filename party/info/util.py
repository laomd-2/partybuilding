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


def filter_first_talk():
    end, month = get_end_time(29)
    groups = group_by_branch(Member.objects.filter(activist_date__isnull=True, application_date__gte=end))
    return month, groups


def filter_activist():
    # 在2个月前交申请书，即2.1或8.1前
    end, month = get_end_time(30)
    groups = group_by_branch(Member.objects.filter(activist_date__isnull=True, application_date__lt=end))
    return month, groups


def filter_key_develop_person():
    end, month = get_end_time(11 * 30)
    groups = group_by_branch(Member.objects.filter(key_develop_person_date__isnull=True,
                                                   activist_date__lt=end))
    return month, groups


def filter_pre_party_member():
    end, month = get_end_time(60)
    groups = group_by_branch(Member.objects.filter(first_branch_conference__isnull=True,
                                                   graduated_party_school_date__isnull=False,
                                                   key_develop_person_date__lt=end))
    return month, groups


def filter_write_application():
    end, month = get_end_time(10 * 30)
    groups = group_by_branch(Member.objects.filter(second_branch_conference__isnull=True,
                                                   first_branch_conference__lt=end))
    return month, groups


def filter_party_member():
    end, month = get_end_time(11 * 30)
    groups = group_by_branch(Member.objects.filter(second_branch_conference__isnull=True,
                                                   first_branch_conference__lt=end))
    return month, groups
