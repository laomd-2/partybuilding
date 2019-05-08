from django.http import HttpResponse, HttpResponseNotFound
from django.utils.encoding import escape_uri_path
from django.views.generic import TemplateView
from .admin import *
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

    @staticmethod
    def export(request, model):
        query = queryset(request, PreMember, fields=model.beian_fields)
        filename = model.beian_template

        doc = Document(filename)
        table = doc.tables[0]

        try:
            UserStyle1 = doc.styles.add_style('UserStyle1', 1)
        except ValueError:
            UserStyle1 = doc.styles['UserStyle1']
        # 设置字体尺寸
        UserStyle1.font.size = Pt(12)
        # 设置中文字体
        UserStyle1.font.name = '仿宋_GB2312'
        UserStyle1._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')

        for row in query:
            row['brith_date'] = '-'.join(row['birth_date'].split('-')[:-1])
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
        filename = filename.split('/')[-1]
        response = HttpResponse(data, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
        return response