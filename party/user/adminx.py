from common.base import AdminObject
from user.util import get_bind_member
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from info.models import Member
import xadmin
from xadmin import views
from common.rules import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        g = Group.objects.get(name='普通成员')
        if created:
            instance.groups.add(g)
    except:
        pass


class UserAdmin(AdminObject):
    list_display = ['username', 'get_member', 'email', 'is_active', 'is_staff', 'last_login']
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
        qs = self.model._default_manager.get_queryset()
        if not is_school_admin(self.request.user):  # 判断是否是管理员
            member = self.bind_member
            if member is None:
                return qs.filter(username=self.request.user)
            if is_branch_manager(self.request.user):  # 支书
                colleges = Member.objects.filter(branch=member.branch)  # 找到该model 里该用户创建的数据
                return qs.filter(username__in=[college.netid for college in colleges])
            elif is_member(self.request.user):
                return qs.filter(username=self.request.user)  # 普通成员
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(is_superuser=False)

    def has_change_permission(self, obj=None):
        if super().has_change_permission(obj):
            if obj is None or self.request.user == obj or is_school_admin(self.request.user):
                return True
            if is_branch_manager(self.request.user):
                m = self.bind_member
                m2 = get_bind_member(obj)
                return m is not None and m2 is not None and m.branch == m2.branch
        return False

    def has_delete_permission(self, request=None, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(self.request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            if is_branch_manager(self.request.user):
                m = self.bind_member
                m2 = get_bind_member(obj)
                return m is not None and m2 is not None and m.branch == m2.branch
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
