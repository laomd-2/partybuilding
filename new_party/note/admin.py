from django.contrib import messages
# Register your models here.
from django.contrib import admin
from common.base import AdminObject
from note.models import *


class NoteAdminBase(AdminObject):
    list_display = ['author', 'title', 'last_edit_time']
    search_fields = ['author', 'title']
    list_filter = ['create_time', 'last_edit_time']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()
        m = request.user.member
        if m is None:
            return self.model.objects.none()
        else:
            return self.model.objects.filter(branch_id=m['branch_id'])

    def save_model(self, request, obj, form, change):
        if change:
            m = request.user.member
            if m is None:
                messages.error(request, '您不是党支部书记。')
                return
            obj.author = m['name']
            obj.branch_id = m['branch_id']
        obj.save()

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if obj is None or request.user.is_superuser:
                return True
            else:
                m = request.user.member
                if m is not None:
                    return m['name'] == obj.author
        return False

    def has_delete_permission(self, request, obj=None):
        if super(NoteAdminBase, self).has_delete_permission(request, obj):
            if obj is None or request.user.is_superuser:
                return True
            else:
                m = request.user.member
                if m is not None:
                    return m['name'] == obj.author
        return False


@admin.register(Note)
class NoteAdmin(NoteAdminBase):
    style_fields = {"content": "ueditor"}


@admin.register(Rule)
class RuleAdmin(NoteAdminBase):
    pass
