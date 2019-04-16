from django.contrib.auth import get_permission_codename

from import_export.formats import base_formats
from user.util import get_bind_member


class AdminObject(object):
    list_export = ('xlsx',)
    formats = base_formats.DEFAULT_FORMATS[2:3]

    @property
    def bind_member(self):
        return get_bind_member(self.request.user)

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and \
                self.user.has_perm('%s.%s' % (self.app_label, codename))

    def has_approve_permission(self):
        codename = get_permission_codename('approve', self.opts)
        return ('approve' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))
