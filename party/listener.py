import wxpy
import time
import datetime
from teaching.models import Sharing
from info.models import Member
from teaching.models import Activity, TakePartIn


def get_activity(title, now):
    if '三十讲' in title or '第' == title[0] and '讲' in title[2:5]:
        try:
            return Activity.objects.get(name='习近平三十讲', date__lte=now, end_time__gte=now)
        except:
            pass
    try:
        return Activity.objects.get(name='学习强国APP学习', date__lte=now, end_time__gte=now)
    except:
        return None


while True:
    bot = wxpy.Bot(cache_path=True, console_qr=2)
    daka = bot.groups().search('计二党支部')
    test = bot.groups().search('测试群')
    @bot.register(daka + test, [wxpy.SHARING, wxpy.TEXT], except_self=False)
    def on_msg(msg):
        now = datetime.datetime.now()
        zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond)
        end = zero + datetime.timedelta(hours=24, minutes=0, seconds=0)
        msg_type = msg.type
        from_user = msg.member.name
        content = msg.text
        
        if msg_type == wxpy.SHARING:
            if Sharing.objects.filter(member__name=from_user, title=content):
                return
        else:
            if len(content) > 255:
                content = content[:252] + '...'
            if len(content) < 50 or Sharing.objects.filter(impression=content):
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
                    except:
                        credit = TakePartIn(member=obj.member, activity=xuexi, credit=xuexi.credit)
                        credit.save()
                    obj.added = True
        obj.save()
    bot.join()
