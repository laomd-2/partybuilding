from django.db.models import Q

from common.base import AdminObject
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from info.models import Member, Branch
import xadmin
from xadmin import views
from common.rules import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            m = instance.member
            if m is not None:
                g = Group.objects.get(name='普通成员')
                instance.groups.add(g)
    except Group.DoesNotExist:
        pass


class UserAdmin(AdminObject):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'last_login']
    search_fields = ['username']

    list_filter = ['is_active', 'is_staff', 'last_login']
    model_icon = 'fa fa-vcard'

    @property
    def exclude(self):
        if self.request.user.is_superuser:
            return []
        return ['is_superuser', 'date_joined', 'user_permissions', 'password']

    @property
    def list_editable(self):
        if is_school_manager(self.request.user):
            return []
        if is_branch_admin(self.request.user):  # 支书
            return ['email', 'is_staff', 'is_active']
        return ['email']

    def get_readonly_fields(self):
        if is_school_admin(self.request.user):
            return ['username', 'is_staff', 'is_active', 'last_login', 'email']
        if is_branch_manager(self.request.user):  # 支书
            return ['groups', 'username', 'last_login']
        return ['groups', 'username', 'is_staff', 'is_active', 'last_login']

    def queryset(self):
        qs = self.model.objects
        if is_school_admin(self.request.user):  # 判断是否是管理员
            # if self.request.user.is_superuser:
            return qs.all()
            # else:
            #     school = int(self.request.user.username[0])
            #     ms = Member.objects.filter(branch__school_id=school).values('netid')
            #     return qs.filter(Q(username=self.request.user.username) |
            #                      Q(username__in=[m['netid'] for m in ms]))
        else:
            member = self.request.user.member
            if member is None or is_member(self.request.user):
                return qs.filter(username=self.request.user)
            if is_branch_manager(self.request.user):  # 支书
                colleges = Member.objects.filter(branch_id=member['branch_id']).values('netid')
                return qs.filter(username__in=[college['netid'] for college in colleges])
        return qs.none()

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if obj is None or self.request.user == obj.username or is_school_admin(self.request.user):
                return True
            if is_branch_manager(self.request.user):
                m = self.request.user.member
                m2 = obj.member
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False

    def has_delete_permission(self, request=None, obj=None):
        if super().has_delete_permission(request, obj):
            if self.request.user.is_superuser:
                return True
            if request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            if is_school_admin(self.request.user):
                m2 = obj.member
                school = int(self.request.user.username[0])
                try:
                    branch = Branch.objects.get(id=m2['branch_id'])
                    return school == branch.school_id
                except:
                    return False
            if is_branch_manager(self.request.user):
                m = self.request.user.member
                m2 = obj.member
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)


@xadmin.sites.register(views.CommAdminView)
class GlobalSettings(object):
    site_title = "计二党建系统"
    # 系统名称
    site_footer = "版权所有@SDCS计算机本科生第二党支部"
    # 底部版权栏
    # menu_style = "accordion"
    #  将菜单栏收起来


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    # 设置主题功能
    enable_themes = True
    use_bootswatch = True
    menu_style = 'accordion'
