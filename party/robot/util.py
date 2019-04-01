from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from info.models import Member, Files
from email.header import make_header
from user.models import User


def get_headers(fields):
    headers = []
    for field in fields:
        try:
            headers.append(Member._meta.get_field(field).verbose_name)
        except FieldDoesNotExist:
            headers.append(getattr(Member, field).short_description)
    return headers


def get_infos(fields, appers):
    infos = []
    for apper in appers:
        info = [apper.netid, apper.name]
        for field in fields:
            info.append(getattr(apper, field))
        infos.append(info)
    return infos


def send_email_to_managers(users, title, appers, fields, phase):
    to_emails = [user.email for user in users if user.email]
    if not to_emails or not appers:
        return
    branch_name = appers[0].branch.branch_name
    subject = title
    text_content = ''

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to_emails)
    context = {
        'branch_name': branch_name,
        'title': title,
        'headers': get_headers(fields),
        'appliers': get_infos(fields, appers),
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
    html_content = render_to_string('notice_manager.html', context)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_to_appliers(title, appliers, fields):
    infos = get_infos(fields, appliers)
    context = {
        'title': title,
        'headers': get_headers(fields),
        'root_url': settings.HOST_IP,
    }
    for applier, info in zip(appliers, infos):
        try:
            user = User.objects.get(username=str(applier.netid))
            to_emails = user.email
            print(to_emails)
            if not to_emails:
                continue
            subject = title
            text_content = ''
            context['name'] = applier.name
            context['applier'] = info
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_emails])
            html_content = render_to_string('notice_member.html', context)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except User.DoesNotExist:
            pass
