import wxpy
import logging
import datetime
from xml.etree import ElementTree as ETree
import xmlrpc.client


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
server = xmlrpc.client.ServerProxy('http://localhost:12345')

while True:
    bot = wxpy.Bot(cache_path=True)
    daka = bot.groups().search('计二党支部')
    test = bot.groups().search('测试群')

    @bot.register(daka + test, [wxpy.SHARING, wxpy.TEXT, wxpy.NOTE], except_self=False)
    def on_msg(msg):
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
                logger.warning("%s 撤回了一条消息。（%s）" % (from_user, revoked_msg.text))
                server.put(from_user, now, 1, revoked_msg.type, revoked_msg.text)
        else:
            logger.info("%s 打卡。（%s）" % (from_user, msg.text))
            server.put(from_user, now, 0, msg_type, msg.text)
    bot.join()