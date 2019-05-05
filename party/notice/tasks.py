from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from info.util import *
from info.models import get_branch_managers
from notice.admin import *
from notice.views import queryset
from notice.util import send_email_to_appliers, send_email_to_managers


def send_email(request, model, manager_title, member_title, phase):
    if not is_school_admin(request.user):
        raise PermissionDenied
    groups = group_by_branch(queryset(request, model))
    branch_managers = get_branch_managers()
    fields = model.fields
    success = []
    for branch, appers in groups.items():
        if branch in branch_managers and branch.branch_name == '计算机本科生第二党支部':
            send_email_to_managers(branch_managers[branch], manager_title, appers,
                                   fields, phase)
            # send_email_to_appliers(member_title, appers, fields)
            success.append(branch.branch_name)
    messages.success(request, '%s：已向%s支书发送邮件！' % (manager_title, ','.join(success)))
    return HttpResponseRedirect('/')


def first_talk(request):
    return send_email(request, FirstTalk, FirstTalk.verbose_name, '首次组织谈话', '首次组织谈话')


def activist(request):
    year, month = get_ym(3, 9)
    return send_email(request, Activist, Activist.verbose_name,
                      '%d月接收入党积极分子' % month, '入党积极分子')


def key_develop_person(request):
    year, month = get_ym(3, 9)
    return send_email(request, KeyDevelop, KeyDevelop.verbose_name,
                      '%d月接收重点发展对象' % month, '重点发展对象')


def learningclass(request):
    year, month = get_ym(4, 10)
    return send_email(request, LearningClass, LearningClass.verbose_name,
                      '%d月党训班学习' % month, -1)


def pre_party_member1(request):
    year, month = get_ym(6, 12)
    return send_email(request, PreMember, PreMember.verbose_name,
                      '%d月接收预备党员' % month, '预备党员')


# def write_application():
#     month, groups = filter_write_application()
#     branch_managers = get_branch_managers()
#     for branch, appers in groups.items():
#         if branch in branch_managers:
#             send_email_to_appliers('递交转正申请书', appers,
#                                    ['application_date',
#                                     'first_branch_conference',
#                                     'write_application_date_end'])


def party_member(request):
    year, month = get_ym(6, 12)
    return send_email(request, FullMember, FullMember.verbose_name,
                      '%d月预备党员转正' % month, '正式党员')
