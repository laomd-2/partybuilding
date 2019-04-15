# Register your models here.
import xadmin
from common.base import AdminObject
from notice.models import *


class ViewObject(AdminObject):

    def has_delete_permission(self, request=None, obj=None):
        return False

    def has_add_permission(self):
        return False

    def has_change_permission(self, obj=None):
        return False


@xadmin.sites.register(FirstTalk)
class FirstTalkAdmin(ViewObject):
    list_display = ['branch', 'netid', 'name', 'application_date', 'talk_date_end']
    model_icon = 'fa fa-hourglass-o'


@xadmin.sites.register(Activist)
class ActivistAdmin(ViewObject):
    list_display = ['branch', 'netid', 'name', 'application_date']
    model_icon = 'fa fa-hourglass-1'


@xadmin.sites.register(KeyDevelop)
class KeyDevelopAdmin(ViewObject):
    list_display = ['branch', 'netid', 'name', 'activist_date']
    model_icon = 'fa fa-hourglass-2'


@xadmin.sites.register(PreMember)
class PreMemberAdmin(ViewObject):
    list_display = ['branch', 'netid', 'name', 'key_develop_person_date']
    model_icon = 'fa fa-hourglass-3'


@xadmin.sites.register(FullMember)
class FullMemberAdmin(ViewObject):
    list_display = ['branch', 'netid', 'name', 'application_date', 'first_branch_conference',
                    'application_fullmember_date']
    model_icon = 'fa fa-hourglass'
