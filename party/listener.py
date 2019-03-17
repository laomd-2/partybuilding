import wxpy
import datetime
import threading
from xml.etree import ElementTree as ETree
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


mutex = threading.Lock()
while True:
    bot = wxpy.Bot(cache_path=True, console_qr=2)
    daka = bot.groups().search('计二党支部')
    test = bot.groups().search('测试群')

    @bot.register(daka + test, [wxpy.SHARING, wxpy.TEXT, wxpy.NOTE], except_self=False)
    def on_msg(msg):
        print(msg)
        msg_type = msg.type
        from_user = msg.member.name
        now = datetime.datetime.now()
        # 处理撤回的消息
        if msg_type == wxpy.NOTE:
            revoked = ETree.fromstring(msg.raw['Content'].replace('&lt;', '<').replace('&gt;', '>')).find('revokemsg')
            if revoked:
                # 根据找到的撤回消息 id 找到 bot.messages 中的原消息
                revoked_msg = bot.messages.search(id=int(revoked.find('msgid').text))[0]
                if not revoked_msg:
                    return
                with mutex:
                    if revoked_msg.type == wxpy.SHARING:
                        sharing = Sharing.objects.get(member__name=from_user, title=revoked_msg.text)
                        sharing.title = None
                    else:
                        sharing = Sharing.objects.get(member__name=from_user, impression=revoked_msg.text)
                        sharing.impression = ''
                    if sharing.title or sharing.impression:
                        if sharing.added:
                            print('去掉学时')
                            sharing.added = False
                            xuexi = get_activity(revoked_msg.text, now)
                            credit = TakePartIn.objects.get(member=sharing.member, activity=xuexi)
                            credit.credit -= xuexi.credit
                            if credit.credit <= 0:
                                credit.delete()
                            else:
                                credit.save()
                        sharing.save()
                    else:
                        sharing.delete()
            return

        zero = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond)
        end = zero + datetime.timedelta(hours=24, minutes=0, seconds=0)
        content = msg.text

        with mutex:
            if msg_type == wxpy.SHARING:
                if Sharing.objects.filter(member__name=from_user, title=content):
                    return
            else:
                if len(content) < 50 or Sharing.objects.filter(impression=content):
                    return
            try:
                obj = Sharing.objects.get(added=False, member__name=from_user, when__gte=zero, when__lt=end)
            except Sharing.DoesNotExist:
                try:
                    m = Member.objects.get(name=from_user)
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
    bot.join()


