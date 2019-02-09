import xadmin
from .models import User
from info.models import Member
from xadmin import views
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        g = Group.objects.get(name='普通成员')
        if created:
            instance.groups.add(g)
    except:
        pass


@xadmin.sites.register(views.CommAdminView)
class GlobalSettings(object):
    site_title = "SDCS党建信息管理系统"
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


class UserAdmin(object):
    list_display = ['username', 'email', 'is_active', 'is_staff']
    search_fields = ['username']

    list_filter = ['username']
    model_icon = 'fa fa-vcard'

    @property
    def exclude(self):
        if self.request.user.is_superuser:
            return []
        return ['is_superuser', 'date_joined', 'user_permissions', 'password']

    @property
    def list_editable(self):
        if self.request.user.has_perm('info.add_branch'):
            return [field.name for field in User._meta.get_fields()]
        if self.request.user.has_perm('info.add_member'):  # 支书
            return UserAdmin.list_display[1:]
        return ['email']

    def get_readonly_fields(self):
        if self.request.user.has_perm('info.add_branch'):
            return []
        if self.request.user.has_perm('info.add_member'):  # 支书
            return ['groups', 'username', 'last_login']
        return ['groups', 'username', 'is_staff', 'is_active', 'last_login']

    def queryset(self):
        # User.objects.get(username='000001').delete()
        if not self.request.user.has_perm('info.add_branch'):  # 判断是否是管理员
            try:
                member = Member.objects.get(netid=self.request.user)
                if self.request.user.has_perm('info.add_member'):  # 支书
                    colleges = Member.objects.filter(branch=member.branch)  # 找到该model 里该用户创建的数据
                    return self.model.objects.filter(username__in=[college.netid for college in colleges])
            except Exception as e:
                print(e)
                pass
            return self.model.objects.filter(username=self.request.user)  # 普通成员
        return self.model.objects.all()


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
