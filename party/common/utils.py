import datetime
import io
import os
import xadmin
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from openpyxl.styles import Font, Alignment


def get_headers(fields, model):
    res = []
    for field in fields:
        try:
            res.append(model._meta.get_field(field).verbose_name)
        except:
            if hasattr(model, field):
                res.append(getattr(model, field).short_description)
            else:
                modeladmin = xadmin.site._registry[model]
                res.append(getattr(modeladmin, field).short_description)
    return res


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
