from django.contrib import messages
# Register your models here.
from django.contrib.auth import get_permission_codename

import xadmin
from common.base import AdminObject
from common.rules import is_school_admin, is_branch_admin
from work.models import *


class NoteAdminBase(AdminObject):
    list_display = ['author', 'title', 'last_edit_time']
    search_fields = ['author', 'title']
    list_filter = ['create_time', 'last_edit_time']

    def queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        m = self.request.user.member
        if m is None:
            return self.model.objects.none()
        else:
            return self.model.objects.filter(branch_id=m['branch_id'])

    def save_models(self):
        if self.org_obj is None:
            m = self.request.user.member
            if m is None:
                messages.error(self.request, '您不是党支部书记。')
                return
            self.new_obj.author = m['name']
            self.new_obj.branch_id = m['branch_id']
        self.new_obj.save()

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if obj is None or self.request.user.is_superuser:
                return True
            else:
                m = self.request.user.member
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
                m = self.request.user.member
                if m is not None:
                    return m['name'] == obj.author
        return False


@xadmin.sites.register(Note)
class NoteAdmin(NoteAdminBase):
    object_list_template = 'article_list.html'
    model_icon = 'fa fa-book'
    style_fields = {"content": "ueditor"}
    list_display_links = ['title']


@xadmin.sites.register(Rule)
class RuleAdmin(NoteAdminBase):
    model_icon = 'fa fa-print'
    list_display = ['author', 'title', 'get_file']

    def get_list_display_links(self):
        if is_branch_admin(self.request.user):
            return ['title']
        return [None, ]


@xadmin.sites.register(Files)
class FilesAdmin(AdminObject):
    list_display = ['name', 'get_notice', 'get_files']
    model_icon = "fa fa-files-o"

    def get_list_display_links(self):
        if is_school_admin(self.request.user):
            return ['name']
        return [None, ]
