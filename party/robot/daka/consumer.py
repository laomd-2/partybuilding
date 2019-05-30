import datetime
import os
import time
import threading
from django.conf import settings
import logging
import wxpy
from info.models import Member
from robot.msg_queue import get
from teaching.models import Activity, Sharing, TakePartIn2
import json
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
lock = threading.Lock()


def get_activity(title, now):
    important = json.load(open(os.path.join(settings.BASE_DIR, '重要活动.json')))
    for pattern, activity in important:
        if re.match(pattern, title):
            try:
                return Activity.objects.filter(name=activity, date__lte=now).first()
            except Activity.DoesNotExist:
                pass
    return None


def consumer():
    while True:
        try:
            with lock:
                consume()
        except Exception as e:
            logger.info(e)
            time.sleep(2)


def consume():
    user, time, revoke, msg_type, content = get()
    now = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if revoke:
        logger.warning("%s 撤回了一条消息。（%s）" % (user, content))
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
                credit = TakePartIn2.objects.get(member=sharing.member, activity=xuexi)
                credit.credit -= xuexi.credit
                if credit.credit <= 0:
                    credit.delete()
                else:
                    credit.save()
            sharing.save()
        else:
            sharing.delete()
    else:
        logger.info("receive a message of type %s。" % ('SHARING' if msg_type == wxpy.SHARING else 'TEXT'))
        zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond)
        end = zero + datetime.timedelta(hours=24, minutes=0, seconds=0)
        if msg_type == wxpy.SHARING:
            if Sharing.objects.filter(member__name=user, title=content).exists():
                logger.info('duplicated title')
                return
        elif msg_type == wxpy.TEXT:
            if len(content) < 50 or Sharing.objects.filter(impression=content).exists():
                logger.info('duplicated content')
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
                            credit = TakePartIn2.objects.get(member_id=obj.member_id, activity_id=xuexi.id)
                            credit.credit += xuexi.credit
                            credit.save()
                    except TakePartIn2.DoesNotExist:
                        credit = TakePartIn2(member_id=obj.member_id, activity_id=xuexi.id, credit=xuexi.credit)
                        credit.save()
                    obj.added = True
        obj.save()
