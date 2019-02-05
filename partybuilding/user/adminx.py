import xadmin
from .models import User
from info.models import Member
from xadmin import views


class GlobalSettings(object):
    site_title = "SDCS党建信息管理系统"
    # 系统名称
    site_footer = "版权所有@SDCS计算机本科生第二党支部"
    # 底部版权栏
    # menu_style = "accordion"
    #  将菜单栏收起来


class BaseSetting(object):
    # 设置主题功能
    enable_themes = True
    use_bootswatch = True


class UserAdmin(object):
    list_display = ['username', 'email', 'is_active', 'is_staff']
    search_fields = ['username']
    list_editable = ['username', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['username']
    model_icon = 'fa fa-user'

    def queryset(self):
        if not self.request.user.is_superuser:  # 判断是否是超级用户
            member = Member.objects.get(netid=self.request.user)
            colleges = Member.objects.filter(branch_name=member.branch_name)  # 找到该model 里该用户创建的数据
            return self.model.objects.filter(username__in=[college.netid for college in colleges])
        return self.model.objects.all()


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
