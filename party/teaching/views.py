from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView
from teaching.models import *


class CheckInView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = '签到'
        context.update(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        activity_id = request.GET.get('activity')
        if activity_id is None:
            return HttpResponseNotFound('未指定会议或活动。')
        try:
            activity = Activity.objects.filter(id=int(activity_id)).values('id', 'name', 'date', 'checkin_code')[0]
            token = get_md5id(activity['id'], activity['checkin_code'])
            if token != request.GET.get('token'):
                return HttpResponseNotFound('二维码已失效。')
        except ValueError:
            return HttpResponseNotFound('会议或活动有误。')
        except IndexError:
            return HttpResponseNotFound('该会议或活动不存在。')
        return render(request, 'checkin.html', context=self.get_context_data(**activity))

    def post(self, request):
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
        except IndexError:
            return HttpResponseNotFound('该会议或活动不存在。')
        try:
            ip = request.META['REMOTE_ADDR']
            username = int(request.POST.get('username'))
            member = Member.objects.get(netid=username)
            try:
                checkin = CheckIn.objects.get(ip=ip, activity_id=activity_id)
            except CheckIn.DoesNotExist:
                checkin = None
            if checkin is not None and checkin.netid != username:
                messages.error(request, '请勿替他人签到。')
            else:
                if member.is_party_member():
                    model = TakePartIn
                else:
                    model = TakePartIn2
                try:
                    take = model.objects.get(member_id=username, activity_id=activity_id)
                    if activity['is_cascade']:
                        messages.info(request, '您已签到成功，请勿重复签到。')
                    else:
                        take.credit += activity['credit']
                        take.save()
                        # 从缺席名单中删除
                        AskForLeave.objects.filter(activity_id=activity_id, member_id=username).delete()
                        messages.success(request, '签到成功。')
                        if not CheckIn.objects.filter(ip=ip, activity_id=activity_id).exists():
                            CheckIn(netid=username, ip=ip, activity_id=activity_id).save()
                except model.DoesNotExist:
                    take = model(member_id=username, activity_id=activity_id, credit=activity['credit'])
                    take.save()
                    # 从缺席名单中删除
                    AskForLeave.objects.filter(activity_id=activity_id, member_id=username).delete()
                    messages.success(request, '签到成功。')
                    CheckIn(netid=username, ip=ip, activity_id=activity_id).save()
        except Exception as e:
            messages.error(request, '您输入的学号有误。')
        return render(request, 'checkin.html', context=self.get_context_data(**activity))
