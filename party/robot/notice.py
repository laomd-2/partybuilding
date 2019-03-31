from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from info.models import Member, Files
from email.header import make_header

from info.util import get_end_time, group_by_branch, get_branch_managers


def send_email(users, title, branch_name, appers, fields, phase):
    to_emails = [user.email for user in users if user.email]
    print(to_emails)
    if not to_emails or not appers:
        return

    subject = title
    text_content = ''
    html_content = """
    亲爱的%s支书：<br />
        <blockquote>您好，%s如下，请做好相关准备工作：
        <p>
        <table width="80%%" border="1" cellspacing="0" margin="0 50%%">
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
    """
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to_emails)
    try:
        o = Files.objects.get(name=Files.phases[phase])
        file = o.notice
        file_name = file.path
        name = file.name
        b = make_header([(name, 'utf-8')]).encode('utf-8')
        try:
            msg.attach(b, open(file_name, 'rb').read())
        except FileNotFoundError:
            pass
        html_content += """
            <p><a href="http://%s%s"><b>%s</b></a></p>
        """ % (settings.HOST_IP, reverse('media', args=[o.files.name]), o.files.name)
    except Files.DoesNotExist:
        pass
    except Exception as e:
        print(e)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def first_talk():
    pass


def activist():
    # 在2个月前交申请书，即2.1或8.1前
    end, month = get_end_time(2)
    groups = group_by_branch(Member.objects.filter(activist_date__isnull=True, application_date__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email(branch_managers[branch], '%d月可接收入党积极分子名单' % month, branch.branch_name, appers,
                       ['application_date'], 0)


def key_develop_person():
    end, month = get_end_time(12)
    groups = group_by_branch(Member.objects.filter(key_develop_person_date__isnull=True,
                                                   activist_date__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email(branch_managers[branch], '%d月可接收重点发展对象名单' % month,
                       branch.branch_name, appers,
                       ['application_date', 'activist_date'], 1)


def pre_party_member1():
    end, month = get_end_time(3)
    groups = group_by_branch(Member.objects.filter(first_branch_conference__isnull=True,
                                                   key_develop_person_date__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email(branch_managers[branch], '%d月可接收预备党员（预审后）名单' % month,
                       branch.branch_name, appers,
                       ['application_date', 'activist_date',
                        'key_develop_person_date', 'graduated_party_school_date'], 3)


def party_member():
    end, month = get_end_time(12)
    groups = group_by_branch(Member.objects.filter(second_branch_conference__isnull=True,
                                                   first_branch_conference__lt=end))

    branch_managers = get_branch_managers()
    for branch, appers in groups.items():
        if branch in branch_managers:
            send_email(branch_managers[branch], '%d月可转正预备党员名单' % month,
                       branch.branch_name, appers,
                       ['application_date', 'first_branch_conference'], 4)
