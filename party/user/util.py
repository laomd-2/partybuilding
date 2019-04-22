from django.db.models import Q
from info.models import Member, School
from teaching.models import Activity
from common.rules import *


def get_bind_member(user):
    try:
        return Member.objects.filter(netid=int(user.username)).values('netid', 'name', 'branch_id')[0]
    except Member.DoesNotExist:
        return None
    except IndexError:
        return None


def get_visuable_activities(user):
    if not is_school_admin(user):  # 判断是否是党辅
        m = get_bind_member(user)
        if m is None:
            return Activity.objects.none()
        return Activity.objects.filter(Q(visualable_others=True)
                                       | Q(branch__id__contains=m['branch_id'])).prefetch_related('branch')
    return Activity.objects.all().prefetch_related('branch')


def get_visuable_members(user):
    qs = Member.objects.select_related('branch')
    if is_branch_manager(user):  # 支书
        member = get_bind_member(user)
        if member is not None:
            return qs.filter(branch_id=member['branch_id'])
    elif is_member(user):
        member = get_bind_member(user)
        return qs.filter(netid=member['netid'])
    elif is_school_manager(user):
        school = School.objects.get(id=int(user.username[0]))
        return Member.objects.filter(branch__school_id=school)
    elif user.is_superuser:
        return qs.all()
    return qs.none()
