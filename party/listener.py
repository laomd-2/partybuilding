import itchat
import datetime
from itchat.content import *
from teaching.models import Sharing
from info.models import Member
from teaching.models import Activity, TakePartIn


itchat.auto_login(hotReload=True, enableCmdQR=2)


@itchat.msg_register([TEXT, SHARING], isMpChat=True, isGroupChat=True)
def xuexi_listener(msg):
    now = datetime.datetime.now()
    zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    end = zero + datetime.timedelta(hours=24, minutes=0, seconds=0)
    try:
        xuexi = Activity.objects.get(name='学习强国APP学习', date__lte=now, end_time__gte=now)
    except:
        return
    room = msg['User']['NickName']
    if room == '计二党支部👉学习群' or room == '计二党支部微信群':
        msg_type = msg['Type']
        from_user = msg['ActualNickName']
        content = msg['Content']
        if len(content) < 50:
            return
        if '-' in from_user:
            from_user = from_user[from_user.find('-') + 1:]
        try:
            obj = Sharing.objects.get(added=False, member__name=from_user)
        except:
            try:
                m = Member.objects.get(name=from_user)
                obj = Sharing(member=m, when=now)
            except Exception as e:
                # itchat.send('学时记录失败了~请先修改备注为姓名。', msg['FromUserName'])
                return
        if msg_type == SHARING:
            try:
                obj.title = content[content.find('<title>') + 7: content.find('</title>')]
            except:
                obj.delete()
        else:
            obj.impression = content[:150]
        if obj.title and obj.impression:
            try:
                count = Sharing.objects.filter(member=obj.member, when__gte=zero, when__lt=end).count()
                if count < 2:
                    credit = TakePartIn.objects.get(member=obj.member, activity=xuexi)
                    credit.credit += xuexi.credit
                    credit.save()
            except:
                credit = TakePartIn(member=obj.member, activity=xuexi, credit=xuexi.credit)
                credit.save()
            obj.added = True
        obj.save()
itchat.run()
