from info.util import *
from .util import send_email_to_appliers, send_email_to_managers


def first_talk():
    groups = filter_first_talk()[1]
    branch_managers = get_branch_managers()
    fields = ['application_date', 'talk_date_end']
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '未谈话入党申请人名单', appers,
                                   fields, 5)
            send_email_to_appliers('首次组织谈话', appers, fields)


def activist():
    month, groups = filter_activist()
    branch_managers = get_branch_managers()
    fields = ['application_date']
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可接收入党积极分子名单' % month, appers,
                                   fields, 0)
            send_email_to_appliers('%d月接收入党积极分子' % month, appers, fields)


def key_develop_person():
    month, groups = filter_key_develop_person()
    fields = ['application_date', 'activist_date']
    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可接收重点发展对象名单' % month,
                                   appers, fields, 1)
            send_email_to_appliers('%d月接收重点发展对象' % month, appers, fields)


def pre_party_member1():
    month, groups = filter_pre_party_member()
    fields = ['application_date', 'activist_date',
              'key_develop_person_date', 'graduated_party_school_date']
    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可接收预备党员（预审后）名单' % month,
                                   appers, fields, 3)
            send_email_to_appliers('%d月接收预备党员' % month, appers, fields)


def write_application():
    month, groups = filter_write_application()
    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_appliers('递交转正申请书', appers,
                                   ['application_date',
                                    'first_branch_conference',
                                    'write_application_date_end'])


def party_member():
    month, groups = filter_party_member()
    fields = ['application_date', 'first_branch_conference']
    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], '%d月可转正预备党员名单' % month,
                                   appers, fields, 4)
            send_email_to_appliers('%d月预备党员转正' % month, appers, fields)
