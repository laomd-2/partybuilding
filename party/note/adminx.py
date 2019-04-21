from django.contrib import admin, messages

# Register your models here.
from django.contrib.auth import get_permission_codename

import xadmin
from common.base import AdminObject
from note.models import Note


@xadmin.sites.register(Note)
class NoteAdmin(AdminObject):
    list_display = ['author', 'title', 'last_edit_time']
    search_fields = ['author', 'title']
    list_filter = ['create_time', 'last_edit_time']
    model_icon = 'fa fa-book'
    style_fields = {"content": "ueditor"}

    def queryset(self):
        if self.request.user.is_superuser:
            return Note.objects.all()
        m = self.bind_member
        if m is None:
            return Note.objects.none()
        else:
            return Note.objects.filter(branch_id=m['branch_id'])

    def save_models(self):
        if self.org_obj is None:
            m = self.bind_member
            if m is None:
                messages.error(self.request, '您不是党支部书记。')
                return
            self.new_obj.author = m['name']
            self.new_obj.branch_id = m['branch']
        self.new_obj.save()

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if obj is None or self.request.user.is_superuser:
                return True
            else:
                m = self.bind_member
                if m is not None:
                    return m['name'] == obj.author
        return False

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        has = ('delete' not in self.remove_permissions) and \
              self.user.has_perm('%s.%s' % (self.app_label, codename))
        if has:
            if obj is None or self.request.user.is_superuser:
                return True
            else:
                m = self.bind_member
                if m is not None:
                    return m['name'] == obj.author
        return False
