import xadmin
from .models import User
from info.models import Member
from xadmin import views


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
    model_icon = 'fa fa-user'
    exclude = ('is_superuser', 'date_joined', 'user_permissions')

    @property
    def list_editable(self):
        if self.request.user.is_superuser:
            return [field.name for field in User._meta.get_fields()]
        if self.request.user.has_perm('user.add_user'):  # 支书
            return UserAdmin.list_display[1:]
        return ['email']

    def get_readonly_fields(self):
        if self.request.user.is_superuser:
            return []
        if self.request.user.has_perm('user.add_user'):  # 支书
            return ['last_login']
        return ['groups', 'username', 'password', 'is_staff', 'is_active', 'last_login']

    def queryset(self):
        if not self.request.user.is_superuser:  # 判断是否是超级用户
            member = Member.objects.get(netid=self.request.user)
            if self.request.user.has_perm('user.add_user'):  # 支书
                colleges = Member.objects.filter(branch=member.branch)  # 找到该model 里该用户创建的数据
                return self.model.objects.filter(username__in=[college.netid for college in colleges])
            return self.model.objects.filter(username=member.netid)  # 普通成员
        return self.model.objects.all()


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
