import os
import re

from django.conf import settings
from django.contrib.auth import get_permission_codename
from import_export.formats import base_formats
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


class AdminObject(object):
    list_export = []
    list_per_page = 15
    formats = base_formats.DEFAULT_FORMATS[2:3]
    excel_template = os.path.join(settings.MEDIA_ROOT, 'Excel模板/空白.xlsx')

    @property
    def bind_member(self):
        return get_bind_member(self.request.user)

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and \
                self.user.has_perm('%s.%s' % (self.app_label, codename))
