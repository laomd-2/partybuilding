from django.contrib.auth import get_permission_codename
from user.models import get_bind_member


class AdminObject(object):
    @property
    def bind_member(self):
        return get_bind_member(self.request.user)

    def has_view_permission(self, obj=None):
        view_codename = get_permission_codename('view', self.opts)
        change_codename = get_permission_codename('change', self.opts)

        return ('view' not in self.remove_permissions) and \
               (self.user.has_perm('%s.%s' % (self.app_label, view_codename)) or
                self.user.has_perm('%s.%s' % (self.app_label, change_codename))
                ) and self.view_(obj)

    def has_add_permission(self):
        codename = get_permission_codename('add', self.opts)
        return ('add' not in self.remove_permissions) and \
               self.user.has_perm('%s.%s' % (self.app_label, codename)) and self.add_()

    def has_change_permission(self, obj=None):
        codename = get_permission_codename('change', self.opts)
        return ('change' not in self.remove_permissions) and \
               self.user.has_perm('%s.%s' % (self.app_label, codename)) and self.change_(obj)

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and \
               self.user.has_perm('%s.%s' % (self.app_label, codename)) and self.delete_(request, obj)

    def view_(self, obj):
        return True

    def add_(self):
        return True

    def change_(self, obj):
        return True

    def delete_(self, reques, obj):
        return True
