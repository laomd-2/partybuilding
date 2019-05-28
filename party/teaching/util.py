from collections import Counter
from django.db.models import Q
from info.models import Member
from teaching.models import Activity, TakePartIn
from common.rules import *


def get_season(now):
    seasons = [datetime.datetime(now.year, m, 1) for m in [2, 5, 8, 11]]
    seasons.append(datetime.datetime(now.year + 1, 2, 1))
    for i in range(1, len(seasons)):
        if now < seasons[i]:
            return seasons[i - 1], seasons[i]


def get_visual_activities(user):
    qs = Activity.objects
    if not is_school_admin(user):  # 判断是否是党辅
        m = user.member
        if m is None:
            return qs.none()
        return qs.filter(Q(visualable_others=True)
                         | Q(branch__id__contains=m['branch_id'])).distinct().prefetch_related('branch')
    return qs.all().distinct().prefetch_related('branch')


def get_visual_credit(user, model=TakePartIn):
    qs = model.objects
    if user.is_superuser:
        return 0, qs.all()
    now = datetime.datetime.today()
    year, month = now.year, now.month
    if month < 2:
        year -= 1

    if is_school_manager(user):
        return year, qs.filter(member__branch__school_id=int(user.username[0])).select_related('member', 'activity')
    m = user.member
    if m is None:
        return year, qs.none()
    else:
        return year, qs.filter(member__branch_id=m['branch_id']).select_related('member', 'activity')


def get_monthly_credit(all_take):
    months = dict()
    for t in all_take:
        d = t.activity.date
        month = "%d/%02d" % (d.year, d.month)
        months.setdefault(month, Counter())
        months[month][t.activity.atv_type] += t.credit
    option = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross',
                'crossStyle': {
                    'color': '#999'
                }
            }
        },
        'toolbox': {
            'feature': {
                'magicType': {'show': True, 'type': ['line', 'bar']},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'legend': {
            'data': Activity.atv_type_choices
        },
        'xAxis': [
            {
                'type': 'category',
                'data': ['%s' % m for m in sorted(months.keys())],
                'axisPointer': {
                    'type': 'shadow'
                }
            }
        ],
        'yAxis': [
            {
                'type': 'value',
                'name': '学时数'
            },
        ],
        'series': [
            {
                'name': name,
                'type': 'bar',
                'data': [months[k][name] for k in sorted(months.keys())]
            } for name in Activity.atv_type_choices
        ]
    }
    return option


def get_credit(all_take, members):
    credit_sum = Counter()
    for m in members:
        credit_sum[m] = 0
    for r in all_take:
        credit_sum[r.member] += r.credit
    credit_sum = list(credit_sum.items())
    credit_sum.sort(key=lambda x: x[1], reverse=True)
    option = {
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
            }
        },
        'toolbox': {
            'feature': {
                'magicType': {'show': True, 'type': ['line', 'bar']},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        # 'grid': {
        #     'left': '3%',
        #     'right': '4%',
        #     'bottom': '3%',
        #     'containLabel': True
        # },
        'xAxis': {
            'type': 'category',
            'data': [x[0].name for x in credit_sum],
            'axisLabel': {
                'rotate': 45
            }
        },
        'yAxis': {
            'type': 'value'
        },
        'series': [{
            'data': [x[1] for x in credit_sum],
            'type': 'bar'
        }]
    }
    return option


def get_detail_chart(request, model, branch=None):
    m = request.user.member
    if m is None and not is_school_manager(request.user):
        return None
    my_charts = {}

    try:
        if branch is None:
            branch = int(request.GET.get('branch')
                         or request.path.split('/')[-3])
    except ValueError:
        return None
    year, all_take = get_visual_credit(request.user, model)
    if is_school_manager(request.user):
        members = Member.objects.filter(branch_id=branch)
        all_take = all_take.filter(member__branch_id=branch)
    else:
        members = Member.objects.filter(branch_id=m['branch_id'])
        all_take = all_take.filter(member__branch_id=m['branch_id'])
    if all_take.count():
        my_charts['ranking'] = {
            'title': '%d年度党员继续教育学时' % year,
            'option': get_credit(all_take, members.filter(first_branch_conference__isnull=False))
        }
    return my_charts


def get_list_chart(request, model):
    m = request.user.member
    if m is None:
        return None
    else:
        branch = m['netid']
    charts = get_detail_chart(request, model, branch)
    charts.update(get_list_chart2(request, model))
    return charts


def get_list_chart2(request, model):
    m = request.user.member
    my_charts = {}

    year, all_take = get_visual_credit(request.user, model)
    all_take = all_take.filter(member_id=m['netid'])
    if all_take.count():
        my_charts['takepartin'] = {
            'title': '%d年度个人学时概览' % year,
            'option': get_monthly_credit(all_take)
        }

    return my_charts
