import datetime

from django.db.models import Q
from teaching.models import Activity, TakePartIn
from common.rules import *


def get_season(now):
    seasons = [datetime.datetime(now.year, m, 1) for m in [2, 5, 8, 11]]
    seasons.append(datetime.datetime(now.year + 1, 2, 1))
    for i in range(1, len(seasons)):
        if now < seasons[i]:
            return seasons[i - 1], seasons[i]


def get_visual_activities(user):
    qs = Activity.objects.distinct().prefetch_related('branch')
    if not is_school_admin(user):  # 判断是否是党辅
        m = user.member
        if m is None:
            return qs.none()
        return qs.filter(Q(visualable_others=True)
                         | Q(branch__id__contains=m['branch_id']))
    return qs.all()


def get_visual_credit(user, model=TakePartIn):
    qs = model.objects.select_related('member', 'activity')
    if user.is_superuser:
        return 0, qs.all()
    now = datetime.datetime.today()
    year, month = now.year, now.month
    if month < 2:
        year -= 1
    qs = qs.filter(activity__date__gte=datetime.date(year, 2, 1),
                   activity__date__lt=datetime.date(year + 1, 2, 1))

    if is_school_manager(user):
        return year, qs.filter(member__branch__school_id=int(user.username[0]))
    m = user.member
    if m is None:
        return year, qs.none()
    else:
        return year, qs.filter(member__branch_id=m['branch_id'])
