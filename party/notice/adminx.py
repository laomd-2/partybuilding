# Register your models here.

import xadmin
from common.base import AdminObject
from common.rules import *
from notice.models import *


class ViewObject(AdminObject):

    def has_delete_permission(self, request=None, obj=None):
        return False

    def has_add_permission(self):
        return False

    def has_change_permission(self, obj=None):
        return False

    def queryset(self):
        if is_member(self.request.user):
            m = self.bind_member
            if m is not None:
                return self.model.objects.filter(netid=m.netid)
        elif is_branch_manager(self.request.user):
            m = self.bind_member
            if m is not None:
                return self.model.objects.filter(branch=m.branch)
        elif is_school_manager(self.request.user):
            school = int(self.request.user.username[0])
            return self.model.objects.filter(branch__school_id=school)
        elif self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.none()


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
