import itchat
import datetime
from itchat.content import *
from teaching.models import Sharing
from info.models import Member
from teaching.models import Activity, TakePartIn

itchat.auto_login(hotReload=True, enableCmdQR=2)


def get_activity(title, now):
    if '三十讲' in title or '第' in title[:4] and '讲' in title[:4]:
        try:
            return Activity.objects.get(name='习近平三十讲', date__lte=now, end_time__gte=now)
        except:
            pass
    try:
        return Activity.objects.get(name='学习强国APP学习', date__lte=now, end_time__gte=now)
    except:
        return None


@itchat.msg_register([TEXT, SHARING], isMpChat=True, isGroupChat=True)
def xuexi_listener(msg):
    now = datetime.datetime.now()
    zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                    microseconds=now.microsecond)
    end = zero + datetime.timedelta(hours=24, minutes=0, seconds=0)
    room = msg['User']['NickName']

    if room == '计二党支部👉学习群' or room == '党建系统测试群':
        msg_type = msg['Type']
        from_user = msg['ActualNickName']
        content = msg['Content']
        if len(content) < 50:
            return

        if msg_type == SHARING:
            content = content[content.find('<title>') + 7: content.find('</title>')]
            if Sharing.objects.filter(member__name=from_user, title=content):
                return
        else:
            if len(content) > 255:
                content = content[:252] + '...'
            if Sharing.objects.filter(impression=content):
                return
        try:
            obj = Sharing.objects.get(added=False, member__name=from_user, when__gte=zero, when__lt=end)
        except:
            try:
                m = Member.objects.get(name=from_user)
                obj = Sharing(member=m, when=now)
            except Exception as e:
                # itchat.send('学时记录失败了~请先修改备注为姓名。', msg['FromUserName'])
                return
        if msg_type == SHARING:
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
                    except:
                        credit = TakePartIn(member=obj.member, activity=xuexi, credit=xuexi.credit)
                        credit.save()
                    obj.added = True
        obj.save()


itchat.run()
