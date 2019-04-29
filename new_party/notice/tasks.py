from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from common.rules import is_school_admin
from info.util import *
from notice.admin import *
from notice.views import queryset
from notice.util import send_email_to_appliers, send_email_to_managers


def send_email(request, model, manager_title, member_title, phase):
    if not is_school_admin(request.user):
        raise PermissionDenied
    groups = group_by_branch(queryset(request, model))
    branch_managers = get_branch_managers()
    fields = model.fields
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email_to_managers(branch_managers[branch], manager_title, appers,
                                   fields, phase)
            # send_email_to_appliers(member_title, appers, fields)
    messages.success(request, '已向%s及对应党支部支书发送邮件！' % manager_title)
    return HttpResponseRedirect('/')


def first_talk(request):
    return send_email(request, FirstTalk, FirstTalk.verbose_name, '首次组织谈话', 5)


def activist(request):
    year, month = get_ym(3, 9)
    return send_email(request, Activist, Activist.verbose_name,
                      '%d月接收入党积极分子' % month, 0)


def key_develop_person(request):
    year, month = get_ym(3, 9)
    return send_email(request, KeyDevelop, KeyDevelop.verbose_name,
                      '%d月接收重点发展对象' % month, 1)


def learningclass(request):
    year, month = get_ym(4, 10)
    return send_email(request, LearningClass, LearningClass.verbose_name,
                      '%d月党训班学习' % month, -1)


def pre_party_member1(request):
    year, month = get_ym(6, 12)
    return send_email(request, PreMember, PreMember.verbose_name,
                      '%d月接收预备党员' % month, 3)


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
                      '%d月预备党员转正' % month, 4)
