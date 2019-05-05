import io
from copy import deepcopy

from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from openpyxl import load_workbook

from common.base import wrap
from common.rules import *
from .admin import *
from info.models import Branch
from info.util import get_visual_branch


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
        school = int(request.user.username[0])
        return model.filter(branch__school_id=school)
    elif request.user.is_superuser:
        return model.filter()
    return Member.objects.none()


def queryset(request, model):
    query = _queryset(request, model).extra(select={'branch_name': 'info_branch.branch_name'}) \
        .values(*(model.fields + ['branch_name']))
    query = list(query)
    if query:
        for q in query:
            q['branch_id'] = q['branch_name']
            del q['branch_name']
            for k, v in q.items():
                if v is None:
                    q[k] = ''
            for first in q.keys():  break
            if first != 'branch_id':
                e = q[model.fields[-1]]
                del q[model.fields[-1]]
                q[model.fields[-1]] = e
    return query


def export(request, model):
    filename = model.verbose_name + '.xlsx'
    qs = queryset(request, model)

    work_book = load_workbook(model.excel_template)
    sheet = work_book.active
    if model.row > 1:
        sheet.cell(1, 1, model.verbose_name)
    for ranges in sheet.merged_cells.ranges:
        if ranges.min_row >= model.row:
            sheet.unmerge_cells(str(ranges))
    style_row = sheet[model.row]
    new_rows = len(qs)
    sheet.insert_rows(model.row + 1, new_rows - 1)
    for i in range(new_rows - 1):
        for new_ceil, ceil in zip(sheet[model.row + i + 1], style_row):
            if ceil.has_style:
                new_ceil._style = deepcopy(ceil._style)

    for i, row in enumerate(qs):
        sheet.cell(i + model.row, 1, i + 1)
        for j, value in enumerate(row.values()):
            value = wrap(value)
            sheet.cell(i + model.row, j + 2, value)
    with NamedTemporaryFile() as tmp:
        work_book.save(tmp.name)
        output = io.BytesIO(tmp.read())
    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    output.close()
    return response


def get_first_talk(request):
    return export(request, FirstTalk)


def get_activist(request):
    return export(request, Activist)


def get_keydevelop(request):
    return export(request, KeyDevelop)


def get_learningclass(request):
    return export(request, LearningClass)


def get_premember(request):
    return export(request, PreMember)


def get_fullmember(request):
    return export(request, FullMember)
