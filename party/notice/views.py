import io
from copy import deepcopy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import escape_uri_path
from django.views.generic import TemplateView
from .admin import *
from info.models import Branch
from info.util import get_visual_branch

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.table import WD_ALIGN_VERTICAL


class TableView(TemplateView):
    table_mapping = dict([(model.__name__.lower(), model) 
            for model in [FirstTalk, Activist, KeyDevelop, LearningClass, PreMember, FullMember]])

    # @login_required(login_url='/')
    def get(self, request, table):
        model = self.table_mapping.get(table)
        if model is not None:
            return self.export(request, model)
        return HttpResponseNotFound('未找到资源')

    @staticmethod
    def export(request, model):
        filename = model.export_filename()
        data = model.export(request)
        response = HttpResponse(data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
        return response


class BeianView(TableView):
   
    def export(request, model):
        fields = ['branch_name'] + model.beian_fields
        query = _queryset(request, PreMember).extra(select={'branch_name': 'info_branch.branch_name'}) \
            .values(*fields)
        
        filename = '材料21：接收预备党员备案表.docx'
        doc = Document(filename)
        table = doc.tables[0]
        
        UserStyle1 = doc.styles.add_style('UserStyle1', 1)
        # 设置字体尺寸
        UserStyle1.font.size = Pt(12)
        # 设置中文字体
        UserStyle1.font.name = '仿宋_GB2312'
        UserStyle1._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')

        if query.exists():
            for row in query:
                tb_row = table.add_row()
                values = list(row.values())
                values.insert(5, '无')
                values.insert(5, '')
                for v, cell in zip(values, tb_row.cells):
                    cell.text = wrap(v)
                    for p in cell.paragraphs:
                        p.style = UserStyle1
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        data = to_bytes(doc)
        response = HttpResponse(data, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
        return response