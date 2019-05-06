import os

from django.conf import settings
from django.contrib.admin import ModelAdmin

from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from import_export.formats.base_formats import XLSX
from user.util import get_bind_member


def wrap(value):
    if callable(value):
        value = value()
    if value is None:
        value = ''
    elif value is True:
        value = '是'
    elif value is False:
        value = '否'
    value = str(value)
    if value.startswith('+86'):
        value = value[3:]
    return value


def get_chinese(s):
    pattern = "[\u4e00-\u9fa5]+"
    regex = re.compile(pattern)
    return regex.findall(s)


def get_old(obj):
    model = type(obj)
    try:
        return model.objects.get(pk=obj.pk)
    except model.DoesNotExist:
        return None
    except TypeError:
        return None


class AdminObject(ModelAdmin):
    list_per_page = 15
    formats = base_formats.DEFAULT_FORMATS[2:3]
    excel_template = os.path.join(settings.MEDIA_ROOT, 'Excel模板/空白.xlsx')


class ImportExportAdmin(ImportExportModelAdmin):
    formats = [XLSX]