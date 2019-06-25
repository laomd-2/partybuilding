import time

import wxpy
import logging
import datetime
from xml.etree import ElementTree as ETree
from robot.msg_queue import put

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# def producer():
#     while True:
#         try:
#             wechat()
#         except Exception as e:
#             logger.info(e)
#             time.sleep(2)


def producer():
    bot = wxpy.Bot(console_qr=2, cache_path='/home/party/party/robot/daka/wechat.pkl')
    daka = bot.groups().search('打卡群')
    bot.file_helper.send('我启动啦！')

    @bot.register(daka, [wxpy.SHARING, wxpy.TEXT, wxpy.NOTE], except_self=False)
    def on_msg(msg):
        msg_type = msg.type
        from_user = msg.member.name
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info("receive a message of type %s。" % msg_type)
        # 处理撤回的消息
        if msg_type == wxpy.NOTE:
            revoked = ETree.fromstring(msg.raw['Content'].replace('&lt;', '<').replace('&gt;', '>')).find('revokemsg')
            if revoked:
                # 根据找到的撤回消息 id 找到 bot.messages 中的原消息
                revoked_msg = bot.messages.search(id=int(revoked.find('msgid').text))[0]
                if not revoked_msg:
                    return
                logger.warning("%s 撤回了一条消息。（%s）" % (from_user, revoked_msg.text))
                put(from_user, now, 1, revoked_msg.type, revoked_msg.text)
        else:
            logger.info("%s 打卡。（%s）" % (from_user, msg.text))
            put(from_user, now, 0, msg_type, msg.text)

    @bot.register([bot.file_helper], [wxpy.TEXT], except_self=False)
    def ask(msg):
        return '亲，我还在线哦！'
    # bot.join()
