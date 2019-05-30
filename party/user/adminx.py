from django.contrib.auth.models import Permission
from django.db.models import Q

from common.base import AdminObject
from django.db.models.signals import post_save
from django.dispatch import receiver

from xadmin.plugins.auth import GroupAdmin
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
    list_display = ['username', '_fullname', 'email', 'last_login']
    search_fields = ['username', '_fullname']

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
        if self.org_obj is None:
            return []
        base = ['username', 'last_login', '_fullname']
        if is_school_admin(self.request.user):
            return base
        return ['groups', 'is_staff', 'is_active'] + base

    def queryset(self):
        qs = self.model.objects
        if is_school_admin(self.request.user):  # 判断是否是管理员
            if self.request.user.is_superuser:
                return qs.all()
            else:
                return qs.filter(is_superuser=False)
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
            m = self.request.user.member
            m2 = obj.member
            if m is None or m2 is None:
                return False
            if is_branch_manager(self.request.user):
                return m['branch_id'] == m2['branch_id']
            else:
                return m['netid'] == m2['netid']
        return False

    def has_delete_permission(self, request=None, obj=None):
        if self.request.user.is_superuser:
            return True
        if super().has_delete_permission(request, obj):
            if request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            if is_school_admin(self.request.user):
                return True
            if is_branch_manager(self.request.user):
                m = self.request.user.member
                m2 = obj.member
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False


class MyGroupAdmin(GroupAdmin):
    list_display = list_display_links = ['name']
    visual_models = ['group', 'user',
                     'branch', 'member', 'oldmember', 'dependency',
                     'activity', 'takepartin', 'takepartin2',
                     'files', 'note', 'rule']

    def get_readonly_fields(self):
        if self.org_obj is None:
            return []
        if self.request.user.is_superuser:
            return []
        return ['name']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'permissions' and is_school_manager(self.request.user):
            where = None
            for model in self.visual_models:
                if where is None:
                    where = Q(codename__iendswith=model)
                else:
                    where |= Q(codename__iendswith=model)
            kwargs["queryset"] = Permission.objects.filter(where)
        return super().formfield_for_dbfield(db_field, **kwargs)


xadmin.site.unregister(User)
xadmin.site.unregister(Group)
xadmin.site.register(User, UserAdmin)
Group._meta.verbose_name = Group._meta.verbose_name_plural = '角色'
xadmin.site.register(Group, MyGroupAdmin)


@xadmin.sites.register(views.CommAdminView)
class GlobalSettings(object):
    site_title = "数据科学与计算机学院学生党建系统"
    # 系统名称
    site_footer = "版权所有@数据科学与计算机学院"
    # 底部版权栏
    # menu_style = "accordion"
    #  将菜单栏收起来


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    # 设置主题功能
    enable_themes = True
    use_bootswatch = True
    menu_style = 'accordion'
