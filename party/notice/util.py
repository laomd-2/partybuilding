from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from common.base import wrap
from work.models import Files
from email.header import make_header

from notice.admin import verbose_name
from user.models import User


def get_infos(fields, appers):
    return [[wrap(getattr(apper, field)) for field in fields] for apper in appers]


def send_email_to_managers(users, title, appers, fields, phase):
    to_emails = [user.email for user in users if user.email]
    if not to_emails:
        return
    branch_name = appers[0].branch.branch_name
    subject = title
    text_content = ''

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to_emails)
    context = {
        'branch_name': branch_name,
        'title': title,
        'headers': verbose_name(fields),
        'appliers': get_infos(fields, appers),
        'root_url': settings.HOST_IP
    }
    try:
        o = Files.objects.get(name=phase)
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

    html_content = render_to_string('email_manager.html', context)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_to_appliers(title, appliers, fields, template='email_member.html'):
    infos = get_infos(fields, appliers)
    context = {
        'title': title,
        'headers': verbose_name(fields),
        'root_url': settings.HOST_IP,
    }
    for applier, info in zip(appliers, infos):
        try:
            user = User.objects.get(username=str(applier.netid))
            to_emails = user.email
            if not to_emails:
                continue
            subject = title
            text_content = ''
            context['name'] = applier.name
            context['applier'] = info
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_emails])
            html_content = render_to_string(template, context)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except User.DoesNotExist:
            pass
