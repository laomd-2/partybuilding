import datetime
import io
import os

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from openpyxl.styles import Font, Alignment
import re


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


def set_font(wb, fontname, begin_row=1):
    font = Font(name=fontname)
    for i, row in enumerate(wb.active.iter_rows()):
        if i < begin_row:
            continue
        for cell in row:
            cell.font = font


def set_align(wb, horizontal, vertical, begin_row=1):
    alignment = Alignment(horizontal=horizontal, vertical=vertical, wrap_text=True)
    for i, row in enumerate(wb.active.iter_rows()):
        if i < begin_row:
            continue
        for cell in row:
            cell.alignment = alignment


def to_bytes(wb):
    with NamedTemporaryFile() as tmp:
        wb.save(tmp.name)
        return io.BytesIO(tmp.read())


def media(var):
    return os.path.join(settings.MEDIA_ROOT, var)


class Cache:
    def __init__(self, ttl):
        self.__ttl = ttl
        self.__cache = (0, None)

    def set(self, v):
        now = datetime.datetime.now()
        self.__cache = (now, v)

    def get(self):
        last, v = self.__cache
        now = datetime.datetime.now()
        if last == 0 or (now - last).seconds > self.__ttl:
            return None
        return v
