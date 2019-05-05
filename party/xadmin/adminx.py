from __future__ import absolute_import

from django.contrib.auth import get_permission_codename
from django.template import loader

import xadmin
from common.rules import is_school_admin
from xadmin.views import BaseAdminPlugin, ListAdminView
from .models import UserSettings, Log
from django.utils.translation import ugettext_lazy as _


class objectsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


class UserSettingsAdmin:
    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))


class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), 
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''

    def has_delete_permission(self, request=None, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return ('delete' not in self.remove_permissions) and self.user.has_perm('%s.%s' % (self.app_label, codename))

    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'


class MyExportAdmin(BaseAdminPlugin):
    my_export = False

    def init_request(self, *args, **kwargs):
        return bool(self.my_export) and is_school_admin(self.request.user)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.importexport.export_member.html',
                                             context=context.flatten()))


xadmin.site.register(UserSettings, UserSettingsAdmin)
xadmin.site.register(Log, LogAdmin)
xadmin.site.register_plugin(MyExportAdmin, ListAdminView)
