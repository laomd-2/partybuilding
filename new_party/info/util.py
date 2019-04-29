import datetime

from django.contrib import messages
from django.db.models import Q

from common.base import get_old, get_chinese
from common.rules import *
from info.models import Member, Branch, School, Dependency


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
        try:
            branch = Member.objects.get(netid=int(manager.username)).branch
            if branch.branch_name != '计算机本科生第二党支部':
                continue
            branch_managers.setdefault(branch, [])
            branch_managers[branch].append(manager)
        except Member.DoesNotExist:
            pass
    return branch_managers


def get_visuable_members(model, user):
    qs = model.objects.select_related('branch')
    if is_branch_manager(user):  # 支书
        member = user.member
        if member is not None:
            return qs.filter(branch_id=member['branch_id'])
    elif is_member(user):
        member = user.member
        return qs.filter(netid=member['netid'])
    elif is_school_manager(user):
        school = School.objects.get(id=int(user.username[0]))
        return qs.filter(branch__school_id=school)
    elif user.is_superuser:
        return Member.objects.all()
    return qs.none()


def get_visual_branch(user):
    if is_school_manager(user):
        school = School.objects.get(id=int(user.username[0]))
        return school.branch_set.all()
    elif is_branch_manager(user) or is_member(user):  # 支书
        member = user.member
        if member is not None:
            return Branch.objects.filter(id=member['branch_id'])
    elif user.is_superuser:
        return Branch.objects.all()

    
def check_date_dep(obj, old):
    errors = []
    for dep in Dependency.objects.filter(Q(scope=0) | Q(scope=1 + int(not obj.is_sysu))):
        from_ = getattr(obj, dep.from_1)
        if isinstance(from_, datetime.datetime):
            from_ = from_.date()
        to = getattr(obj, dep.to)
        if isinstance(to, datetime.datetime):
            to = to.date()
        from_2 = None if old is None else getattr(old, dep.from_1)
        to2 = None if old is None else getattr(old, dep.to)
        if (from_ != from_2 or to != to2) and from_ and to:
            delta = to - from_
            if delta.days < dep.days:
                errors.append((dep.from_1, dep.to, delta.days,
                               dep.days_mapping[dep.days]))
    return errors


def check_first_talk_date(obj, old):
    if obj.first_talk_date and obj.application_date:
        if old is None or (obj.application_date != old.application_date or
                           obj.first_talk_date != old.first_talk_date):
            days = (obj.first_talk_date - obj.application_date).days
            return days < 31
    return True


def get_members(branch, names):
    res = []
    for name in names:
        try:
            res.append(Member.objects.filter(branch_id=branch, name=name).first())
        except Member.DoesNotExist:
            pass
    return res


def check_fields(request, obj, msg=messages.error):
    old = get_old(obj)

    errors = check_date_dep(obj, old)
    for e in errors:
        msg(request, "%s到%s需要%s，而%s只用了%d天。"
            % (Member._meta.get_field(e[0]).verbose_name.strip('时间'),
               Member._meta.get_field(e[1]).verbose_name.strip('时间'),
               e[3], obj, e[2]))
        return False
    # 检查首次组织谈话时间
    if obj.is_sysu and not check_first_talk_date(obj, old):
        msg(request, '未在一个月内完成首次组织谈话。')
        return False
    # 检查入党介绍人
    if obj.is_sysu and old is None or obj.recommenders != old.recommenders:
        for m in get_members(obj.branch_id, get_chinese(str(obj.recommenders))):
            if not m.is_real_party_member():
                msg(request, '入党介绍人%s不是正式党员。' % m.name)
                return False
    return True
