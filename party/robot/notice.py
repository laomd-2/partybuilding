from info.models import Member
from info.util import get_end_time, group_by_branch, get_branch_managers
from .util import send_email_to_appliers, send_email_to_managers


def first_talk():
    end, month = get_end_time(29)
    groups = group_by_branch(Member.objects.filter(activist_date__isnull=True, application_date__gte=end))
    branch_managers = get_branch_managers()
    fields = ['application_date', 'talk_date_end']
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '未谈话入党申请人名单', appers,
                                   fields, 5)
            send_email_to_appliers('首次组织谈话', appers, fields)


def activist():
    # 在2个月前交申请书，即2.1或8.1前
    end, month = get_end_time(30)
    groups = group_by_branch(Member.objects.filter(activist_date__isnull=True, application_date__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可接收入党积极分子名单' % month, appers,
                                   ['application_date'], 0)


def key_develop_person():
    end, month = get_end_time(11 * 30)
    groups = group_by_branch(Member.objects.filter(key_develop_person_date__isnull=True,
                                                   activist_date__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可接收重点发展对象名单' % month,
                                   appers, ['application_date', 'activist_date'], 1)


def pre_party_member1():
    end, month = get_end_time(60)
    groups = group_by_branch(Member.objects.filter(first_branch_conference__isnull=True,
                                                   graduated_party_school_date__isnull=False,
                                                   key_develop_person_date__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            title = '%d月可接收预备党员（预审后）名单' % month
            fields = ['application_date', 'activist_date',
                      'key_develop_person_date', 'graduated_party_school_date']
            send_email_to_managers(branch_managers[branch], title, appers,
                                   fields, 3)
            # send_email_to_appliers(title, appers, fields, 3)


def write_application():
    end, month = get_end_time(10 * 30)
    groups = group_by_branch(Member.objects.filter(second_branch_conference__isnull=True,
                                                   first_branch_conference__lt=end))
    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可转正预备党员名单' % month,
                                   appers, ['application_date', 'first_branch_conference'], 4)


def party_member():
    end, month = get_end_time(11 * 30)
    groups = group_by_branch(Member.objects.filter(second_branch_conference__isnull=True,
                                                   first_branch_conference__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可转正预备党员名单' % month,
                                   appers, ['application_date', 'first_branch_conference'], 4)
