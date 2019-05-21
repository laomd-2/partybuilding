from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from common.utils import wrap
from common.rules import *
from work.models import Files
from email.header import make_header
from info.models import Member
from user.models import User


def verbose_name(fields, model=Member):
    res = []
    for field in fields:
        try:
            res.append(model._meta.get_field(field).verbose_name)
        except:
            res.append(getattr(model, field).short_description)
    return res


def get_infos(fields, appers):
    return [[wrap(apper[field]) for field in fields] for apper in appers]


def make_email_to_managers(users, title, appers, fields, phase):
    to_emails = [user['email'] for user in users if user['email']]
    if not to_emails:
        return
    branch_name = appers[0]['branch'].branch_name
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
    return msg


def make_email_to_appliers(title, appliers, fields, template='email_member.html'):
    infos = get_infos(fields, appliers)
    context = {
        'title': title,
        'headers': verbose_name(fields),
        'root_url': settings.HOST_IP,
    }

    mails = []
    for applier, info in zip(appliers, infos):
        try:
            user = User.objects.filter(username=str(applier['netid'])).values('email')[0]
            to_emails = user['email']
            if not to_emails:
                continue
            subject = title
            text_content = ''
            context['name'] = applier['name']
            context['applier'] = info
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to_emails])
            html_content = render_to_string(template, context)
            msg.attach_alternative(html_content, "text/html")
            mails.append(msg)
        except IndexError:
            pass
    return mails


def _queryset(request, model):
    if is_member(request.user):
        m = request.user.member
        if m is not None:
            return model.filter(netid=m['netid'])
    elif is_branch_manager(request.user):
        m = request.user.member
        if m is not None:
            return model.filter(branch_id=m['branch_id'])
    elif is_school_manager(request.user):
        school = request.user.school_id
        return model.filter(branch__school_id=school)
    elif request.user.is_superuser:
        return model.filter()
    return Member.objects.none()


def queryset(request, model, fields=None):
    if fields is None:
        fields = model.fields
    query = _queryset(request, model).extra(select={'branch_name': 'info_branch.branch_name',
                                                    'grade': '2000 + netid div 1000000'}) \
        .values(*(fields + ['branch_name', 'remarks']))
    if query.exists():
        query = list(query)
        for q in query:
            for k, v in q.items():
                if v is None:
                    q[k] = ''
            q['branch'] = q['branch_name']
            del q['branch_name']
            for first in q.keys():  break
            if first != 'branch':   # 确保党支部在第一列
                e = q[fields[-1]]
                del q[fields[-1]]
                q[fields[-1]] = e
    else:
        query = []
    return query


def insert_rows(sheet, row, new_rows):
    for ranges in sheet.merged_cells.ranges:
        if ranges.min_row >= row:
            sheet.unmerge_cells(str(ranges))
    style_row = sheet.row_dimensions[row]
    sheet.insert_rows(row + 1, new_rows - 1)
    for i in range(1, new_rows):
        sheet.row_dimensions[row + i].height = style_row.height
        for cell, new_cell in zip(sheet[row], sheet[row + i]):
            new_cell._style = cell._style
