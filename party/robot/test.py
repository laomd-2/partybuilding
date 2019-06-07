import werobot
import requests
import json
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

params = {
    'appid': 'wx993c596513503d47',
    'secret': '3c12fef307df4f8f4663331534599a01'
}
url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
response = json.loads(requests.get(url, params=params).text)

robot = werobot.WeRoBot(token=response['access_token'])


@robot.handler
def hello(message):
    logger.info(message.content)


robot.run()