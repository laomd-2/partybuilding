from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from info.models import Member, Files
from email.header import make_header
from user.models import User


def send_email_to_managers(users, title, appers, fields, phase):
    to_emails = [user.email for user in users if user.email]
    if not to_emails or not appers:
        return
    branch_name = appers[0].branch.branch_name

    subject = title
    text_content = ''
    headers = []
    for field in fields:
        try:
            headers.append(Member._meta.get_field(field).verbose_name)
        except FieldDoesNotExist:
            headers.append(getattr(Member, field).short_description)
    infos = []

    for apper in appers:
        info = [apper.netid, apper.name]
        for field in fields:
            info.append(getattr(apper, field))
        infos.append(info)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to_emails)
    context = {
        'branch_name': branch_name,
        'title': title,
        'headers': headers,
        'appliers': infos,
        'root_url': settings.HOST_IP,
    }
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
        context['filename'] = o.files.name
    except Files.DoesNotExist:
        pass
    except Exception as e:
        print(e)
    html_content = render_to_string('develop_manager.html', context)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_to_appliers(title, appliers, fields, phase):
    for applier in appliers:
        try:
            user = User.objects.get(username=str(applier.netid))
            to_emails = user.email
            if not to_emails:
                continue
            print(to_emails)
            subject = title
            text_content = ''
            html_content = """
                亲爱的%s同学：<br />
                    <blockquote>您好，%s拟接收你为%s，请做好相关准备工作：
                    <p>
                    <table width="80%%" border="1" cellspacing="0" margin="0 50%%">
                        <tr>
                            <th>学号</th>
                            <th>姓名</th>
                """ % (applier.name, applier.branch.branch_name, Files.phases[phase])
            for field in fields:
                html_content += '<th>%s</th>' % Member._meta.get_field(field).verbose_name
            html_content += '</tr>'

            html_content += """
                    <tr>
                        <td align="center">%d</td>
                        <td align="center">%s</td>
                """ % (applier.netid, applier.name)
            for field in fields:
                html_content += '<td align="center">%s</td>' % getattr(applier, field)
            html_content += '</tr>'
            html_content += """
                    </table></p></blockquote>
                    <p align="right"><a href="http://%s">中山大学数据科学与计算机学院党建</a><br />请勿回复</p>
                """ % settings.HOST_IP
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_emails])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except User.DoesNotExist:
            pass
