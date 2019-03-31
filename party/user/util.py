from django.db.models import Q

from info.models import Member
from teaching.models import Activity
from common.rules import *


def get_bind_member(user):
    try:
        return Member.objects.get(netid=int(user.username))
    except:
        return None


def get_visuable_activities(user):
    qs = Activity.objects.all().distinct()
    if not is_school_admin(user):  # 判断是否是党辅
        m = get_bind_member(user)
        if m is None:
            return qs.none()
        return qs.filter(Q(branch__id__contains=m.branch.id) |
                         Q(visualable_others=True))
    return qs


def get_visuable_members(user):
    qs = Member.objects.all()
    if not is_school_admin(user):  # 判断是否是党辅
        member = get_bind_member(user)
        # print(member)
        if member is None:
            return qs.none()
        else:
            if is_branch_manager(user):  # 支书
                return qs.filter(branch=member.branch)
            elif is_member(user):
                return qs.filter(netid=member.netid)  # 普通成员
            else:
                return qs.none()
    return qs
