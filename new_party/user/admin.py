from django.contrib.auth.admin import GroupAdmin
from django.db.models.signals import post_save
from django.dispatch import receiver
from new_party.admin import *


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


class UserAdmin(BaseModelAdmin):
    list_display = ['username', '_fullname', 'email', 'last_login']
    search_fields = ['username', '_fullname']
    list_editable = ['email']
    list_filter = ['is_active', 'is_staff', 'last_login']
    model_icon = 'fa fa-vcard'
    
    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['is_superuser', 'date_joined', 'user_permissions', 'password']

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        base = ['username', 'last_login', '_fullname']
        if is_school_admin(request.user):
            return base
        return ['groups', 'is_staff', 'is_active'] + base

    def get_queryset(self, request):
        qs = self.model.objects
        if is_school_admin(request.user):  # 判断是否是管理员
            if request.user.is_superuser:
                return qs.all()
            else:
                return qs.filter(is_superuser=False)
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
                m2 = obj.member
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if super().has_delete_permission(request, obj):
            if request is None and obj is None:
                return True
            elif obj is None:
                obj = request
            if is_school_admin(request.user):
                return True
            if is_branch_manager(request.user):
                m = request.user.member
                m2 = obj.member
                return m is not None and m2 is not None and m['branch_id'] == m2['branch_id']
        return False


site.register(Group, GroupAdmin)
site.register(User, UserAdmin)
