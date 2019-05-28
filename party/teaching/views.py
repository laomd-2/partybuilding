from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from teaching.models import *
from user.adminx import GlobalSettings


def checkin(request):
    activity_id = request.GET.get('activity')
    if activity_id is None:
        return HttpResponseNotFound('该会议或活动不存在。')
    try:
        activity_id = int(activity_id)
        activity = Activity.objects.filter(id=activity_id).values('id', 'name', 'date', 'credit',
                                                                  'is_cascade', 'checkin_code')[0]
        token = get_md5id(activity['id'], activity['checkin_code'])
        if token != request.GET.get('token'):
            return HttpResponseNotFound('二维码已失效。')
    except ValueError:
        return HttpResponseNotFound('会议或活动有误。')
    context = {
        'site_title': GlobalSettings.site_title,
        'title': '签到'
    }
    try:
        member = request.user.member
        context['netid'] = member['netid']
        if member.is_party_member():
            model = TakePartIn
        else:
            model = TakePartIn2
        try:
            take = model.objects.get(member_id=member['netid'], activity_id=activity_id)
            if activity['is_cascade']:
                messages.info(request, '您已签到成功，请勿重复签到。')
            else:
                take.credit += activity['credit']
                take.save()
                # 从缺席名单中删除
                AskForLeave.objects.filter(activity_id=activity_id, member_id=member['netid']).delete()
                messages.success(request, '签到成功。')
        except model.DoesNotExist:
            take = model(member_id=member['netid'], activity_id=activity_id, credit=activity['credit'])
            take.save()
            # 从缺席名单中删除
            AskForLeave.objects.filter(activity_id=activity_id, member_id=member['netid']).delete()
            messages.success(request, '签到成功。')
        context['credit'] = take.credit
    except Exception as e:
        messages.error(request, '未找到您的动态信息。')
    context.update(**activity)
    return render(request, 'checkin.html', context=context)
