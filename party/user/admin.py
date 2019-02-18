from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from info.models import Member


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        g = Group.objects.get(name='普通成员')
        if created:
            instance.groups.add(g)
    except:
        pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'last_login']
    search_fields = ['username']

    list_filter = ['username']
    model_icon = 'fa fa-vcard'

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['is_superuser', 'date_joined', 'user_permissions', 'password']
    #
    # def get_list_editable(self, request, **kwargs):
    #     if request.user.has_perm('info.add_branch'):
    #         return [field.name for field in User._meta.get_fields()]
    #     if request.user.has_perm('info.add_member'):  # 支书
    #         return UserAdmin.list_display[1:]
    #     return ['email']

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('info.add_branch'):
            return []
        if request.user.has_perm('info.add_member'):  # 支书
            return ['username', 'last_login']
        return ['groups', 'username', 'is_staff', 'is_active', 'last_login']

    def get_queryset(self, request, **kwargs):
        # User.objects.get(username='000001').delete()
        if not request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            try:
                member = Member.objects.get(netid=request.user)
                if request.user.has_perm('info.add_member'):  # 支书
                    colleges = Member.objects.filter(branch=member.branch)  # 找到该model 里该用户创建的数据
                    return self.model.objects.filter(username__in=[college.netid for college in colleges])
            except Exception as e:
                print(e)
                pass
            return self.model.objects.filter(username=request.user)  # 普通成员
        return self.model.objects.all()


admin.site.site_header = 'SDCS党建信息管理系统'
admin.site.site_title = 'SDCS党建信息管理系统'
admin.site.site_footer = "版权所有@SDCS计算机本科生第二党支部"
