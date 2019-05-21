from django.contrib import messages
# Register your models here.
from new_party.admin import *
from work.models import *


class NoteAdminBase(BaseModelAdmin):
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
        if super().has_delete_permission(request, obj):
            if obj is None or request.user.is_superuser:
                return True
            else:
                m = request.user.member
                if m is not None:
                    return m['name'] == obj.author
        return False


class NoteAdmin(NoteAdminBase):
    model_icon = 'fa fa-book'
    style_fields = {"content": "ueditor"}
    list_display_links = ['title']


class RuleAdmin(NoteAdminBase):
    model_icon = 'fa fa-print'
    list_display = ['author', 'title', 'get_file']

    def get_list_display_links(self, request, list_display):
        if is_branch_admin(request.user):
            return ['title']
        return [None, ]


class FilesAdmin(BaseModelAdmin):
    list_display = ['name', 'get_notice', 'get_files']
    model_icon = "fa fa-files-o"

    def get_list_display_links(self, request, list_display):
        if is_school_admin(request.user):
            return ['name']
        return [None, ]


site.register(Note, NoteAdmin)
site.register(Rule, RuleAdmin)
site.register(Files, FilesAdmin)
