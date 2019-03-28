from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import datetime, os
from django.contrib.auth.models import Group
from info.models import Member, Files
from email.header import make_header


def send_email(users, title, branch_name, appers, fields):
    to_emails = [user.email for user in users if user.email]
    if not to_emails or not appers:
        return

    subject = title
    text_content = ''
    html_content = """
    亲爱的%s支书：<br />
        <blockquote>您好，%s如下，请做好相关准备工作：
        <p>
        <table width="60%%" border="1" cellspacing="0" margin="0 50%%">
            <tr>
                <th>学号</th>
                <th>姓名</th>
    """ % (branch_name, branch_name + title)
    for field in fields:
        html_content += '<th>%s</th>' % Member._meta.get_field(field).verbose_name
    html_content += '</tr>'

    for apper in appers:
        html_content += """
            <tr>
                <td align="center">%d</td>
                <td align="center">%s</td>
        """ % (apper.netid, apper.name)
        for field in fields:
            html_content += '<td align="center">%s</td>' % getattr(apper, field)
        html_content += '</tr>'
    html_content += """
        </table></p></blockquote>
        <p align="right">中山大学数据科学与计算机学院党建<br />请勿回复</p>
        <p><b>需要提交的材料请以党建群最新版本为主。</b></p>
    """
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to_emails)
    try:
        o = Files.objects.get(name='积极分子')
        file = o.notice
        file_name = file.path
        name = file.name
        b = make_header([(name, 'utf-8')]).encode('utf-8')
        msg.attach(b, open(file_name, 'rb').read())
    except Files.DoesNotExist:
        pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def first_talk():
    pass


def activist():
    now = datetime.datetime.now()
    # 在2.1或8.1前交申请书
    end = datetime.datetime(now.year, now.month - 1, 1)

    appers = Member.objects.filter(activist_date__isnull=True, application_date__lt=end)
    groups = dict()
    for apper in appers:
        groups.setdefault(apper.branch, [])
        groups[apper.branch].append(apper)
    group = Group.objects.get(name='党支部管理员')
    managers = group.user_set.all()
    branch_managers = dict()
    for manager in managers:
        branch = Member.objects.get(netid=int(manager.username)).branch
        if branch.id != 1:
            continue
        branch_managers.setdefault(branch, [])
        branch_managers[branch].append(manager)
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email(branch_managers[branch], '%d月可接收入党积极分子名单' % now.month, branch.branch_name, appers,
                       ['application_date'])


def key_develop_person():
    pass


def pre_party_member():
    pass


def party_member():
    pass
