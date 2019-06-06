import sys


def wechat():
    ignore = ['makemigrations', 'migrate', 'collectstatic', 'crontab']
    for i in ignore:
        if i in sys.argv:
            break
    else:
        from robot.daka.producer import producer
        producer()
        return True
    return False
