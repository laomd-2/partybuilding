from django.contrib import admin
from django.db.models import Q

from common.base import AdminObject
from user.util import get_bind_member
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from info.models import Member
from common.rules import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        g = Group.objects.get(name='普通成员')
        if created:
            instance.groups.add(g)
    except:
        pass


@admin.register(User)
class UserAdmin(AdminObject):
    list_display = ['username', 'get_member', 'email', 'is_active', 'is_staff', 'last_login']
    search_fields = ['username']

    list_filter = ['is_active', 'is_staff', 'last_login']
    model_icon = 'fa fa-vcard'

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['is_superuser', 'date_joined', 'user_permissions', 'password']

    def get_readonly_fields(self, request, obj=None):
        if is_school_admin(request.user):
            return ['username', 'is_staff', 'is_active', 'last_login', 'email']
        if is_branch_manager(request.user):  # 支书
            return ['groups', 'username', 'last_login']
        return ['groups', 'username', 'is_staff', 'is_active', 'last_login']

    def get_queryset(self, request):
        qs = self.model.objects
        if is_school_admin(request.user):  # 判断是否是管理员
            if request.user.is_superuser:
                return qs.all()
            else:
                school = int(request.user.username[0])
                ms = Member.objects.filter(branch__school_id=school).values('netid')
                return qs.filter(Q(username=request.user.username) |
                                 Q(username__in=[m['netid'] for m in ms]))
        else:
            member = request.user.member
            if member is None or is_member(request.user):
                return qs.filter(username=request.user)
            if is_branch_manager(request.user):  # 支书
                colleges = Member.objects.filter(branch_id=member['branch_id']).values('netid')
                return qs.filter(username__in=[college['netid'] for college in colleges])
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if super().has_change_permission(request, obj):
            if obj is None or request.user == obj.username or is_school_admin(request.user):
                return True
            if is_branch_manager(request.user):
                m = request.user.member
                m2 = get_bind_member(obj)
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False

    def has_delete_permission(self, request, obj=None):
        if super().has_delete_permission(request, obj):
            if is_school_admin(request.user) or request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            if is_branch_manager(request.user):
                m = request.user.member
                m2 = get_bind_member(obj)
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False
