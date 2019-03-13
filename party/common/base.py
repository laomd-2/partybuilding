from django.contrib.auth import get_permission_codename
from .user_util import get_bind_member


class AdminObject(object):
    list_export = ('xlsx', 'xls')

    @property
    def bind_member(self):
        return get_bind_member(self.request.user)

    # def has_delete_permission(self, request=None, obj=None):
    #     codename = get_permission_codename('delete', self.opts)
    #     return ('delete' not in self.remove_permissions) and \
    #             self.user.has_perm('%s.%s' % (self.app_label, codename))
