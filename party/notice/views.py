import io
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path


# Create your views here.
from xlsxwriter import Workbook

from common.rules import *
from .models import *
from user.util import get_bind_member


def queryset(request, model):
    if is_member(request.user):
        m = get_bind_member(request.user)
        if m is not None:
            return model.filter(netid=m.netid)
    elif is_branch_manager(request.user):
        m = get_bind_member(request.user)
        if m is not None:
            return model.filter(branch=m.branch)
    elif is_school_manager(request.user):
        school = int(request.user.username[0])
        return model.filter(branch__school_id=school)
    elif request.user.is_superuser:
        return model.filter()
    return Member.objects.none()


def export(request, model, filename):
    filename += '.xlsx'
    qs = queryset(request, model)
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True})
    bold = workbook.add_format({'bold': True, 'font_color': 'red'})
    worksheet = workbook.add_worksheet()
    col_width = [0] * len(model.fields)
    header = verbose_name(model.fields)
    for j, f in enumerate(header):
        col_width[j] = max(col_width[j], len(f.encode('gbk')))
        worksheet.write(0, j, f, bold)
    for i, m in enumerate(qs):
        for j, field in enumerate(model.fields):
            f = getattr(m, field) or ""
            if callable(f):
                f = f()
            f = str(f)
            col_width[j] = max(col_width[j], len(f.encode('gbk')))
            worksheet.write(i + 1, j, f)
    for i, width in enumerate(col_width):
        worksheet.set_column(i, i, width)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    output.close()
    return response


def get_first_talk(request):
    return export(request, FirstTalk, '首次组织谈话')


def get_activist(request):
    return export(request, Activist, '%d年%d月可接收入党积极分子' % get_ym(3, 9))


def get_keydevelop(request):
    return export(request, KeyDevelop, '%d年%d月可接收重点发展对象' % get_ym(3, 9))


def get_premember(request):
    return export(request, PreMember, '%d年%d月可接收预备党员' % get_ym(6, 12))


def get_fullmember(request):
    return export(request, FullMember, '%d年%d月可转正预备党员' % get_ym(6, 12))
