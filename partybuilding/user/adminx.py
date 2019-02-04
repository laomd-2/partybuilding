import xadmin
from .models import User
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
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']
    list_editable = ['username', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['username']
    model_icon = 'fa fa-user'


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
