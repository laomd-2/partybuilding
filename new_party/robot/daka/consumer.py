import datetime
import os

from django.conf import settings

import wxpy
from info.models import Member
from robot.msg_queue import get
from teaching.models import Activity, Sharing, TakePartIn
import json


def get_activity(title, now):
    important = json.load(os.path.join(settings.BASE_DIR, '重要活动.json'))
    for profile, activity in important:
        if profile in title:
            try:
                return Activity.objects.get(name=activity, date__lte=now, end_time__gte=now)
            except Activity.DoesNotExist:
                pass
    return None


def consume():
    while True:
        try:
            consumer()
        except:
            pass


def consumer():
    user, time, revoke, msg_type, content = get()
    now = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if revoke:
        if msg_type == wxpy.SHARING:
            sharing = Sharing.objects.get(member__name=user, title=content)
            sharing.title = None
        else:
            sharing = Sharing.objects.get(member__name=user, impression=content)
            sharing.impression = ''
        if sharing.title or sharing.impression:
            if sharing.added:
                sharing.added = False
                xuexi = get_activity(content, now)
                credit = TakePartIn.objects.get(member=sharing.member, activity=xuexi)
                credit.credit -= xuexi.credit
                if credit.credit <= 0:
                    credit.delete()
                else:
                    credit.save()
            sharing.save()
        else:
            sharing.delete()
    else:
        zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond)
        end = zero + datetime.timedelta(hours=24, minutes=0, seconds=0)
        if msg_type == wxpy.SHARING:
            if Sharing.objects.filter(member__name=user, title=content):
                return
        elif msg_type == wxpy.TEXT:
            if len(content) < 50 or Sharing.objects.filter(impression=content):
                return
        try:
            obj = Sharing.objects.get(added=False, member__name=user, when__gte=zero, when__lt=end)
        except Sharing.DoesNotExist:
            try:
                m = Member.objects.get(name=user)
                obj = Sharing(member=m, when=now)
            except Member.DoesNotExist:
                return

        if msg_type == wxpy.SHARING:
            obj.title = content
        else:
            obj.impression = content
        if obj.title and obj.impression:
            if not obj.member.first_branch_conference and \
                    not obj.member.second_branch_conference:
                xuexi = get_activity(obj.title, now)
                if xuexi is not None:
                    try:
                        count = Sharing.objects.filter(member=obj.member,
                                                       when__gte=zero,
                                                       when__lt=end, added=True).count()
                        if count < 4:
                            credit = TakePartIn.objects.get(member=obj.member, activity=xuexi)
                            credit.credit += xuexi.credit
                            credit.save()
                    except TakePartIn.DoesNotExist:
                        credit = TakePartIn(member=obj.member, activity=xuexi, credit=xuexi.credit)
                        credit.save()
                    obj.added = True
        obj.save()
